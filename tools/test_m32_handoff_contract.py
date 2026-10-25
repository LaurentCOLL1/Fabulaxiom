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
        self.assertEqual(x["expected_tests"], 60)
        self.assertEqual(x["browser_new_cases"], 2)
        self.assertEqual(x["browser_total_expected"], 50)
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
        self.assertEqual(x["expected_tests"], 60)
        self.assertEqual(x["browser_total_expected"], 50)
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
        # PR #108 has its own immutable historical CI record; never inspect the latest main_ci_post_merge here.
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
        self.assertEqual(x["merged_pr"], 110)
        self.assertEqual(x["merge_sha"], "2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b")
        self.assertEqual(x["pr_head_sha"], "f69e36a24aedda15222bb3a4e3a198ba57d0174a")
        self.assertEqual(x["pr_ci"]["run_id"], 39577527093)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39591429432)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["vitest"], 55)
        self.assertEqual(x["chromium_per_mode"], 48)
        self.assertTrue(x["fiction_only"])
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #110 fusionnée", self.doc)


    def test_35_scene_world_proof_remains_fiction_only(self):
        x = self.data["m3_2_product_progress"]["scene_world_proof_candidate"]
        self.assertEqual(x["status"], "MERGED_SOURCE_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["unit_total_expected"], 60)
        self.assertEqual(x["browser_total_expected"], 50)
        self.assertEqual(x["narration_world_inference"], "NEVER")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertIn("preuves du monde par révisions exactes", self.doc)


    def test_36_pr112_merge_keeps_real_gates_closed(self):
        x = self.data["post_pr112_normalization"]
        self.assertEqual(x["merged_pr"], 112)
        self.assertEqual(x["merge_sha"], "3c489aa727129e4b090e2e80a49a93fb3fa95877")
        self.assertEqual(x["pr_head_sha"], "56c5d4d55a616469cda36c5fef7f63369a08bdb2")
        self.assertEqual(x["pr_ci"]["run_id"], 39596187154)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39597532619)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertTrue(x["fiction_only"])
        self.assertEqual(x["vitest"], 60)
        self.assertEqual(x["chromium_per_mode"], 50)
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #112 fusionnée", self.doc)

    def test_37_pr113_merge_and_postmerge_ci_without_gate_promotion(self):
        x = self.data["post_pr113_normalization"]
        self.assertEqual(x["merged_pr"], 113)
        self.assertEqual(x["merge_sha"], "e74f1001c01eff1f37c8b35d97d4ef34f6fbccb3")
        self.assertEqual(x["pr_head_sha"], "6fd369de970e6e35d42c2162f197eb57009a1d42")
        self.assertEqual(x["pr_ci"]["run_id"], 39605681206)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39607280677)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #113", self.doc)

    def test_38_independent_parallelism_only_sequential_writes_and_stops(self):
        p = self.data["execution_parallelism"]
        self.assertEqual(p["policy"],
                         "PARALLEL_WHEN_INDEPENDENT_WITH_EXCLUSIVE_WRITES_AND_SEQUENTIAL_MERGES")
        self.assertEqual(p["policy_document"], "docs/continuity/HANDOFF_PROTOCOL.md")
        self.assertTrue(p["separate_branches_or_worktrees_for_mutations"])
        self.assertEqual(p["shared_branch_or_file_writes"], "SERIAL_ONLY")
        self.assertEqual(p["protected_main_merges"],
                         "SERIAL_EXACT_HEAD_CI_AND_EXPECTED_HEAD_SHA")
        self.assertEqual(p["windows_operator_execution"], "SEPARATE_EXPLICIT_APPROVAL_REQUIRED")
        self.assertEqual(p["real_sqlite_or_sidecars"], "PROHIBITED")
        self.assertEqual(p["gate_promotion"], "NONE_BY_PARALLELISM")
        self.assertEqual(p["m3_2_acceptance"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertIn("Règle permanente — paralléliser", self.policy)
        self.assertIn("expected_head_sha", self.policy)
        self.assertIn("tâches sont indépendantes", self.index)
        self.assertIn("PR #113", self.doc)
        self.assertEqual(self.data["pr35"], "OPEN_DRAFT")
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_39_post_pr114_normalized_at_immutable_exact_ci(self):
        x = self.data["post_pr114_normalization"]
        self.assertEqual(x["merged_pr"], 114)
        self.assertEqual(x["merge_sha"], "ddb23311f40f09c04983b164ccd7afa361698ea8")
        self.assertEqual(x["pr_head_sha"], "8262659d58045c127fe4ee3ac56e6dd5681a9f5f")
        self.assertEqual(x["pr_ci"]["run_id"], 39612803528)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39614175650)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["policy"],
                         "PARALLEL_WHEN_INDEPENDENT_WITH_EXCLUSIVE_WRITES_AND_SEQUENTIAL_MERGES")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #114", self.doc)

    def test_40_pr35_reconciliation_is_only_public_path_overlap(self):
        x = self.data["pr35_reconciliation"]
        self.assertEqual(x["pr"], 35)
        self.assertEqual(x["status"], "PRELIMINARY_PUBLIC_PATH_OVERLAP_NOT_MERGE_AUTHORIZATION")
        self.assertEqual(x["main_ahead_commits"], 472)
        self.assertEqual(x["target_main_sha"], "ddb23311f40f09c04983b164ccd7afa361698ea8")
        self.assertEqual(x["pr_changed_paths"], 84)
        self.assertEqual(len(x["potential_overlapping_paths"]), 7)
        self.assertEqual(x["exact_text_conflicts"], "NOT_DETERMINED")
        self.assertFalse(x["public_mergeable"])
        self.assertFalse(x["rebase_or_reset_performed"])
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertTrue((ROOT / x["source_only_plan"]).is_file())
        self.assertIn("M3_2_PR35_SAFE_RECONCILIATION_PLAN.md", self.doc)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")
        self.assertEqual(self.data["governance"]["prospective"], "NOT_STARTED")


    def test_41_pr115_postmerge_ci_is_exact_and_no_private_gate_was_promoted(self):
        x = self.data["post_pr115_normalization"]
        self.assertEqual(x["merged_pr"], 115)
        self.assertEqual(x["merge_sha"], "33846c8c6813acda5eda5089827f81df99175d2c")
        self.assertEqual(x["pr_head_sha"], "3f1c5676f7035398b61bc143a16eae5e115cdfbe")
        self.assertEqual(x["pr_ci"]["run_id"], 39619267259)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39620942276)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39620942276)
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #115 fusionnée", self.doc)

    def test_42_rust_m32_port_is_compile_test_only_synthetic_sqlite(self):
        c = self.data["m3_2_product_progress"]["test_only_rust_first_stage"]
        self.assertEqual(c["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(c["compiled_only_during_tests"])
        self.assertFalse(c["uses_original_sqlite"])
        self.assertEqual(c["rust_test_cases"], 6)
        self.assertEqual(c["auto_migration_max"], 6)
        self.assertEqual(c["real_tauri_ipc"], "NONE")
        self.assertEqual(c["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(c["real_g3"], "STOP_UNAVAILABLE")
        lib = (ROOT / "src-tauri" / "src" / "lib.rs").read_text(encoding="utf-8")
        self.assertIn("#[cfg(test)]" + chr(10) + "mod m32_manual_chronology;", lib)
        source = (ROOT / "src-tauri" / "src" / "m32_manual_chronology.rs").read_text(encoding="utf-8")
        for function_name in c["functions"]:
            self.assertIn("pub fn " + function_name, source)
        self.assertIn("Connection::open_in_memory()", source)
        self.assertNotIn("#[tauri::command]", source)
        self.assertNotIn("Connection::open(", source)
        self.assertIn("portage limité", self.doc)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_43_pr116_merged_exact_ci_without_real_runtime_promotion(self):
        x = self.data["post_pr116_normalization"]
        self.assertEqual(x["merged_pr"], 116)
        self.assertEqual(x["merge_sha"], "388cb745888f9f2d4d0a07fce1ed19fad9b4a548")
        self.assertEqual(x["pr_head_sha"], "0b2555833c1a2c0152cba2185c8122f3d3ecbbae")
        self.assertEqual(x["pr_ci"]["run_id"], 39626827246)
        self.assertEqual(x["pr_ci"]["rust_tests"], 106)
        self.assertEqual(x["main_ci"]["run_id"], 39628479487)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39628479487)
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #116 fusionnée", self.doc)

    def test_44_second_stage_decisions_are_candidate_ram_only(self):
        x = self.data["m3_2_product_progress"]["test_only_rust_second_stage"]
        self.assertEqual(x["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(x["compiled_only_during_tests"])
        self.assertEqual(x["new_rust_tests"], 6)
        self.assertEqual(x["auto_migration_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        rust = (ROOT / "src-tauri" / "src" / "m32_manual_chronology.rs").read_text(encoding="utf-8")
        for name in x["functions"]:
            self.assertIn("pub fn " + name, rust)
        self.assertIn("db.execute_batch(M32_DECISIONS)", rust)
        sql = (ROOT / x["sql_candidate"]).read_text(encoding="utf-8")
        self.assertIn("SECOND-STAGE TEST-ONLY", sql)
        self.assertNotIn("schema_migrations", sql)
        self.assertNotIn("#[tauri::command]", rust)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_45_pr117_merged_exact_ci_and_private_gates_remain_closed(self):
        x = self.data["post_pr117_normalization"]
        self.assertEqual(x["merged_pr"], 117)
        self.assertEqual(x["merge_sha"], "b76e6c00c579bee36c194872e3679c48fe9788fa")
        self.assertEqual(x["pr_head_sha"], "99d78a46e61a0765b6673353900cea55eb039e74")
        self.assertEqual(x["pr_ci"]["run_id"], 39653506345)
        self.assertEqual(x["pr_ci"]["rust_tests"], 112)
        self.assertEqual(x["main_ci"]["run_id"], 39655214998)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["run_id"], 39655214998)
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #117 fusionnée", self.doc)

    def test_46_restatement_third_stage_is_only_ram_fixture_not_operator(self):
        x = self.data["m3_2_product_progress"]["test_only_rust_third_stage"]
        self.assertEqual(x["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(x["compiled_only_during_tests"])
        self.assertEqual(x["new_rust_tests"], 5)
        self.assertEqual(x["auto_migration_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        src = (ROOT / "src-tauri" / "src" / "m32_manual_chronology.rs").read_text(encoding="utf-8")
        for method in x["functions"]:
            self.assertIn("pub fn " + method, src)
        self.assertIn("db.execute_batch(M32_RESTATEMENTS)", src)
        schema = (ROOT / x["sql_candidate"]).read_text(encoding="utf-8")
        self.assertIn("STAGE 4: test-only", schema)
        self.assertNotIn("schema_migrations", schema)
        self.assertNotIn("#[tauri::command]", src)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_47_pr118_merge_is_exact_and_real_gate_not_promoted(self):
        x = self.data["post_pr118_normalization"]
        self.assertEqual(x["merged_pr"], 118)
        self.assertEqual(x["merge_sha"], "a0942b9566d6de21cf73e55dce47c3797dcb7c81")
        self.assertEqual(x["pr_head_sha"], "ff996fc27da6df12697d68a46b8580a3a33e30b3")
        self.assertEqual(x["pr_ci"]["run_id"], 39658544037)
        self.assertEqual(x["pr_ci"]["rust_tests"], 117)
        self.assertEqual(x["main_ci"]["run_id"], 39660168071)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #118 MERGED", self.doc)

    def test_48_ram_restatement_withdrawals_do_not_promote_chain_or_runtime(self):
        x = self.data["m3_2_product_progress"]["test_only_rust_fourth_stage"]
        self.assertEqual(x["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(x["compiled_only_during_tests"])
        self.assertEqual(x["new_rust_tests"], 4)
        self.assertEqual(x["auto_migration_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["chain_promotion"], "NONE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        rust = (ROOT / "src-tauri" / "src" / "m32_manual_chronology.rs").read_text(encoding="utf-8")
        for name in x["functions"]:
            self.assertIn("pub fn " + name, rust)
        self.assertIn("db.execute_batch(M32_REVOCATIONS)", rust)
        self.assertNotIn("#[tauri::command]", rust)
        schema = (ROOT / x["sql_candidate"]).read_text(encoding="utf-8")
        self.assertIn("in-memory candidate only", schema)
        self.assertNotIn("schema_migrations", schema)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_49_pr119_exact_head_source_qualified_without_windows_acceptance(self):
        x = self.data["post_pr119_normalization"]
        self.assertEqual(x["merged_pr"], 119)
        self.assertEqual(x["merge_sha"], "61e07deaf10fc393c567e8f1960874b75d81adc4")
        self.assertEqual(x["pr_head_sha"], "0df96696e4abefe692f8a0fdca3ab10e726fa9d3")
        self.assertEqual(x["pr_ci"]["run_id"], 39661776335)
        self.assertEqual(x["pr_ci"]["rust_tests"], 121)
        self.assertEqual(x["main_ci"]["run_id"], 39684342539)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #119 MERGED", self.doc)

    def test_50_one_successor_stage_remains_ram_only_and_partial_order(self):
        x = self.data["m3_2_product_progress"]["test_only_rust_fifth_stage"]
        self.assertEqual(x["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(x["compiled_only_during_tests"])
        self.assertEqual(x["max_successors_per_withdrawn_restatement"], 1)
        self.assertTrue(x["partial_order_only"])
        self.assertEqual(x["auto_migration_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        src = (ROOT / "src-tauri" / "src" / "m32_manual_chronology.rs").read_text(encoding="utf-8")
        for method in x["functions"]:
            self.assertIn("pub fn " + method, src)
        self.assertIn("db.execute_batch(M32_SUCCESSORS)", src)
        self.assertNotIn("#[tauri::command]", src)
        sql = (ROOT / x["sql_candidate"]).read_text(encoding="utf-8")
        self.assertIn("ONE guarded successor", sql)
        self.assertNotIn("schema_migrations", sql)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_51_pr120_merged_with_terminal_exact_main_ci_no_operator_authority(self):
        x = self.data["post_pr120_normalization"]
        self.assertEqual(x["merged_pr"], 120)
        self.assertEqual(x["merge_sha"], "01766707a347a269b283c2aa7ea02f44979759e9")
        self.assertEqual(x["pr_head_sha"], "f7ef3ceeaee40bb90e1cb9fe180121f11867fc28")
        self.assertEqual(x["pr_ci"]["run_id"], 39685054113)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["main_ci"]["run_id"], 39686405108)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertIn("PR #120 fusionnée", self.doc)


    def test_52_pr121_merged_documentary_only_and_no_operator_promotion(self):
        x = self.data["post_pr121_normalization"]
        self.assertEqual(x["merged_pr"], 121)
        self.assertEqual(x["merge_sha"], "08caad24e20eae484e94fd084edb487b5c370bd5")
        self.assertEqual(x["pr_head_sha"], "6a1a22dedaa4e3d2c302a56959083017578dc7da")
        self.assertEqual(x["pr_ci"]["run_id"], 39713440057)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["main_ci"]["run_id"], 39716352685)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertIn("PR #121", self.doc)

    def test_53_terminal_successor_revocation_requires_ram_fixtures_and_stops(self):
        x = self.data["m3_2_product_progress"]["test_only_rust_sixth_stage"]
        self.assertEqual(x["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(x["compiled_only_during_tests"])
        self.assertEqual(x["new_rust_tests"], 3)
        self.assertEqual(x["auto_migration_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["chain_promotion"], "NONE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        source = (ROOT / "src-tauri/src/m32_manual_chronology.rs").read_text(encoding="utf-8")
        for method in x["functions"]:
            self.assertIn("pub fn " + method, source)
        self.assertIn("db.execute_batch(M32_SUCCESSOR_REVOCATIONS)", source)
        self.assertNotIn("#[tauri::command]", source)
        schema = (ROOT / x["sql_candidate"]).read_text(encoding="utf-8")
        self.assertIn("Test-only append-only retirement", schema)
        self.assertIn("successor revocation immutable", schema)
        self.assertNotIn("schema_migrations", schema)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_54_pr122_terminal_source_ci_is_test_only_not_operator_gate(self):
        x = self.data["post_pr122_normalization"]
        self.assertEqual(x["merged_pr"], 122)
        self.assertEqual(x["merge_sha"], "52b06099ba0cff0da15fa697b0e2043afc883a00")
        self.assertEqual(x["pr_head_sha"], "1ade25c7b8c500d712c452a08d90ed26a1ffbe89")
        self.assertEqual(x["merge_sha"], "52b06099ba0cff0da15fa697b0e2043afc883a00")
        self.assertEqual(x["pr_ci"]["run_id"], 39717330885)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 128)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 53)
        self.assertEqual(x["main_ci"]["run_id"], 39718851557)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["job_steps"], 74)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["merge_sha"], "52b06099ba0cff0da15fa697b0e2043afc883a00")
        self.assertTrue(x["no_recursive_chain"])
        self.assertEqual(x["normal_runtime_sqlite_schema_max"], 6)
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertIn("PR #122", self.doc)


    def test_55_pr123_documentary_normalization_passed_no_windows_gates(self):
        x = self.data["post_pr123_normalization"]
        self.assertEqual(x["merged_pr"], 123)
        self.assertEqual(x["merge_sha"], "a3c4112b335bba69e3d5d4fa4673ae05f1a57241")
        self.assertEqual(x["pr_head_sha"], "f72f1dd51d50661af7dfab39f4059e7a25940472")
        self.assertEqual(x["merge_sha"], "a3c4112b335bba69e3d5d4fa4673ae05f1a57241")
        self.assertEqual(x["pr_ci"]["run_id"], 39719646691)
        self.assertEqual(x["pr_ci"]["attempt"], 2)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 128)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 54)
        self.assertEqual(x["main_ci"]["run_id"], 39720904972)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertIn("PR #123", self.doc)

    def test_56_recursive_chain_candidate_is_ram_only_and_not_product_authority(self):
        x = self.data["m3_2_product_progress"]["test_only_rust_seventh_stage"]
        self.assertEqual(x["status"], "MERGED_TEST_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertTrue(x["compiled_only_during_tests"])
        self.assertEqual(x["new_rust_tests"], 4)
        self.assertEqual(x["auto_migration_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertTrue(x["requires_retired_parent"])
        self.assertTrue(x["append_only_history"])
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        source = (ROOT / "src-tauri/src/m32_manual_chronology.rs").read_text(encoding="utf-8")
        for name in x["functions"]:
            self.assertIn("pub fn " + name, source)
        self.assertIn("db.execute_batch(M32_CHAIN)", source)
        self.assertNotIn("#[tauri::command]", source)
        schema = (ROOT / x["sql_candidate"]).read_text(encoding="utf-8")
        self.assertIn("stage 8: recursive append-only correction lineage", schema)
        self.assertNotIn("schema_migrations", schema)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_57_pr124_protected_merge_only_fictional_ram_and_stops(self):
        x = self.data["post_pr124_normalization"]
        self.assertEqual(x["merged_pr"], 124)
        self.assertEqual(x["merge_sha"], "db09722076561d35dcc0fe3495e21cf0d0ceef9f")
        self.assertEqual(x["pr_head_sha"], "1fdbe18b163dc8caa48bfde439a36b93b81c848a")
        self.assertEqual(x["merge_sha"], "db09722076561d35dcc0fe3495e21cf0d0ceef9f")
        self.assertEqual(x["pr_head_sha"], "1fdbe18b163dc8caa48bfde439a36b93b81c848a")
        self.assertEqual(x["pr_ci"]["run_id"], 39721484412)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 132)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 56)
        self.assertEqual(x["main_ci"]["run_id"], 39723495236)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["normal_runtime_sqlite_schema_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertIn("PR #124", self.doc)


    def test_58_pr125_protected_handoff_records_only_source_success(self):
        x = self.data["post_pr125_normalization"]
        self.assertEqual(x["merged_pr"], 125)
        self.assertEqual(x["merge_sha"], "4b14afbc7fe8de607429e795b656179724d7ee7f")
        self.assertEqual(x["pr_head_sha"], "8ce7bb3ae2295662dfba8f4b5961f9394f1e771f")
        self.assertEqual(x["merge_sha"], "4b14afbc7fe8de607429e795b656179724d7ee7f")
        self.assertEqual(x["pr_head_sha"], "8ce7bb3ae2295662dfba8f4b5961f9394f1e771f")
        self.assertEqual(x["pr_ci"]["run_id"], 39723734278)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 132)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 57)
        self.assertEqual(x["main_ci"]["run_id"], 39726331901)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["main_ci"]["job_steps"], 74)
        self.assertEqual(x["main_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["merge_sha"], "4b14afbc7fe8de607429e795b656179724d7ee7f")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["normal_runtime_sqlite_schema_max"], 6)
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertIn("PR #125", self.doc)


    def test_59_pr126_source_only_merge_does_not_promote_runtime(self):
        x = self.data["post_pr126_normalization"]
        self.assertEqual(x["merged_pr"], 126)
        self.assertEqual(x["merge_sha"], "7c4ff2f84bb67b51c8ca01eef0f9ca78a1bfe8d9")
        self.assertEqual(x["pr_head_sha"], "0a5f972472eec1e53cd2621ca1fb3d6955e5f18f")
        self.assertEqual(x["merge_sha"], "7c4ff2f84bb67b51c8ca01eef0f9ca78a1bfe8d9")
        self.assertEqual(x["pr_head_sha"], "0a5f972472eec1e53cd2621ca1fb3d6955e5f18f")
        self.assertEqual(x["pr_ci"]["run_id"], 39727486056)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 132)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 58)
        self.assertEqual(x["main_ci"]["run_id"], 39748359823)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["normal_runtime_sqlite_schema_max"], 6)
        self.assertIn("PR #126", self.doc)

    def test_60_react_history_ui_candidate_is_isolated_fictional_only(self):
        x = self.data["m3_2_product_progress"]["test_only_react_correction_history"]
        self.assertEqual(x["status"], "MERGED_FICTIONAL_BROWSER_ONLY_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["new_unit_tests"], 8)
        self.assertEqual(x["chromium_scenarios_per_mode"], 53)
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["tauri_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["network_access"], "NONE")
        self.assertEqual(x["storage_access"], "NONE")
        self.assertFalse(x["editing_authorized"])
        self.assertFalse(x["real_g3_authorized"])
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        source = (ROOT / x["ui_component"]).read_text(encoding="utf-8")
        fixture = (ROOT / x["synthetic_browser_lab"]).read_text(encoding="utf-8")
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        self.assertIn("auditM32FictionalCorrectionChain", source)
        self.assertIn("M32FictionalCorrectionHistory", fixture)
        self.assertNotIn("M32FictionalCorrectionHistory", app)
        self.assertNotIn("@tauri-apps", source)
        self.assertNotIn("localStorage", source)
        self.assertNotIn("fetch(", source)
        self.assertNotIn("<button", source)
        runner = (ROOT / "tools/m32_browser_interaction.cjs").read_text(encoding="utf-8")
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 62/62", runner)
        self.assertEqual(self.data["g2a"]["absence_of_sqlite_writer"], "NOT_PROVEN")


    def test_61_pr127_protected_merge_keeps_browser_history_outside_runtime(self):
        x = self.data["post_pr127_normalization"]
        self.assertEqual(x["merged_pr"], 127)
        self.assertEqual(x["merge_sha"], "dd578161f1c84554c03434d0f1066f65d6e53dc6")
        self.assertEqual(x["pr_head_sha"], "d71288e5f7a046c6e90131118de5cecd8a6ee5cb")
        self.assertEqual(x["merge_sha"], "dd578161f1c84554c03434d0f1066f65d6e53dc6")
        self.assertEqual(x["pr_head_sha"], "d71288e5f7a046c6e90131118de5cecd8a6ee5cb")
        self.assertEqual(x["pr_ci"]["run_id"], 39749304955)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 132)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 60)
        self.assertEqual(x["pr_ci"]["chromium_normal"], 53)
        self.assertEqual(x["pr_ci"]["chromium_strict_csp"], 53)
        self.assertEqual(x["pr_ci"]["strict_pinned_fictional_blobs"], 11)
        self.assertEqual(x["main_ci"]["run_id"], 39750459759)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["tauri_ipc"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertIn("PR #127", self.doc)


    def test_62_pr128_protected_documentary_normalization_not_operator_acceptance(self):
        x = self.data["post_pr128_normalization"]
        self.assertEqual(x["merge_sha"], "593b39e531e2a93e2f334220f37f6d8ed9bf9c93")
        self.assertEqual(x["pr_head_sha"], "ab5d7ed9cc0d9aafe4803d2b5b40d7b9bd23cabd")
        self.assertEqual(x["pr_ci"]["run_id"], 39751125802)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 132)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 61)
        self.assertEqual(x["pr_ci"]["chromium_normal"], 53)
        self.assertEqual(x["pr_ci"]["chromium_strict_csp"], 53)
        self.assertEqual(x["main_ci"]["run_id"], 39755042137)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        observed = self.data["post_pr128_postmain_terminal_observation"]
        self.assertEqual(observed["source_pr"], 128)
        self.assertEqual(observed["merge_sha"], x["merge_sha"])
        self.assertEqual(observed["run_id"], 39755042137)
        self.assertEqual(observed["conclusion"], "SUCCESS")
        self.assertEqual(observed["job_steps"], 74)
        self.assertEqual(self.data["post_pr128_postmain_terminal_observation"]["conclusion"], "SUCCESS")
        observed = self.data["post_pr127_postmain_terminal_observation"]
        self.assertEqual(observed["source_pr"], 127)
        self.assertEqual(observed["merge_sha"], "dd578161f1c84554c03434d0f1066f65d6e53dc6")
        self.assertEqual(observed["run_id"], 39750459759)
        self.assertEqual(observed["conclusion"], "SUCCESS")
        self.assertEqual(observed["job_steps"], 74)
        self.assertEqual(self.data["post_pr127_normalization"]["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertIn("PR #128", self.doc)

    def test_63_pr129_documentary_checkpoint_is_not_runtime_authority(self):
        x = self.data["post_pr129_normalization"]
        self.assertEqual(x["merged_pr"], 129)
        self.assertEqual(x["pr_ci"], {"run_id": 39756548081, "conclusion": "SUCCESS", "job_steps": 74})
        self.assertEqual(x["main_ci"], {"run_id": 39758153975, "conclusion": "SUCCESS", "job_steps": 74})
        self.assertTrue(x["historical_pr127_snapshot_unchanged"])
        self.assertTrue(x["historical_pr128_snapshot_unchanged"])
        for pr in (127, 128):
            self.assertEqual(self.data[f"post_pr{pr}_normalization"]["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(self.data["post_pr128_postmain_terminal_observation"]["conclusion"], "SUCCESS")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["normal_runtime_sqlite_schema_max"], 6)
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertIn("PR #129", self.doc)
        self.assertIn("39758153975", self.doc)

    def test_64_pr130_protected_merge_without_operator_promotion(self):
        x = self.data["post_pr130_normalization"]
        self.assertEqual(x["merged_pr"], 130)
        self.assertEqual(x["merge_sha"], "8f330a4feff30092847e5bf180160efed174ebdd")
        self.assertEqual(x["pr_head_sha"], "f980e8e294f537f6b588ded56f6f79cc772558d6")
        self.assertEqual(x["pr_ci"]["run_id"], 39764830760)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["job_steps"], 74)
        self.assertEqual(x["pr_ci"]["rust_tests"], 132)
        self.assertEqual(x["pr_ci"]["handoff_tests"], 63)
        self.assertEqual(x["main_ci"]["run_id"], 39769613787)
        self.assertEqual(x["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertIn("PR #130", self.doc)

    def test_65_fictional_predecessor_witness_is_not_chronology_authority(self):
        x = self.data["m3_2_product_progress"]["test_only_react_predecessor_provenance"]
        self.assertEqual(x["status"], "SOURCE_CANDIDATE_NEW_CI_REQUIRED_NOT_PRODUCT_ACCEPTED")
        self.assertEqual(x["existing_vitest_total"], 8)
        self.assertEqual(x["existing_chromium_total_per_mode"], 53)
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["network_access"], "NONE")
        self.assertEqual(x["tauri_ipc"], "NONE")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertFalse(x["editing_authorized"])
        self.assertFalse(x["global_chronology_inferred"])
        for key in ("document", "component", "tests", "browser"):
            self.assertTrue((ROOT / x[key]).is_file())
        src = (ROOT / x["component"]).read_text(encoding="utf-8")
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        browser = (ROOT / x["browser"]).read_text(encoding="utf-8")
        self.assertIn("Corrige explicitement", src)
        self.assertIn("ancienne assertion", src)
        self.assertIn("Aucun ordre global déduit", src)
        self.assertNotIn("M32FictionalCorrectionHistory", app)
        self.assertNotIn("@tauri-apps", src)
        self.assertNotIn("fetch(", src)
        self.assertNotIn("localStorage", src)
        self.assertIn("Corrige explicitement fiction-successor", browser)
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 62/62", browser)
        self.assertIn("PR #130", self.doc)

    def test_66_pr131_fictional_predecessor_merge_does_not_accept_real_m32(self):
        x = self.data["post_pr131_normalization"]
        self.assertEqual(x["merged_pr"], 131)
        self.assertEqual(x["merge_sha"], "37d8aa100e9d6fe61bbe6650f554a147661e703e")
        self.assertEqual(x["pr_head_sha"], "6b1973e077e90885d326cb5acbb2358368523bd2")
        self.assertEqual(x["pr_ci"], {"run_id": 39770785693, "conclusion": "SUCCESS", "job_steps": 74,
                                       "rust_tests": 132, "handoff_tests": 65, "chromium_normal": 53,
                                       "chromium_strict_csp": 53})
        self.assertEqual(x["failed_earlier_ci"]["run_id"], 39770570255)
        self.assertEqual(x["failed_earlier_ci"]["conclusion"], "FAILURE")
        self.assertEqual(x["main_ci"], {"run_id": 39776433056, "conclusion": "IN_PROGRESS_AT_CHECKPOINT"})
        self.assertEqual(self.data["post_pr130_normalization"]["main_ci"]["conclusion"],
                         "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(self.data["post_pr130_postmain_terminal_observation"]["conclusion"], "SUCCESS")
        self.assertEqual(self.data["post_pr130_postmain_terminal_observation"]["run_id"], 39769613787)
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["normal_runtime_sqlite_schema_max"], 6)
        self.assertEqual(x["ui"], "FICTIONAL_BROWSER_ONLY_PREDECESSOR_DISPLAY")
        self.assertIn("PR #131", self.doc)

    def test_67_pr132_protected_merge_keeps_real_m32_gates_closed(self):
        x = self.data["post_pr132_normalization"]
        self.assertEqual(x["merged_pr"], 132)
        self.assertEqual(x["merge_sha"], "202152a3e502b08e6b7b77344769b6b0a1ea76bf")
        self.assertEqual(x["pr_head_sha"], "0ccc9af60075e90942d6e0bd7e2f92694bbe4876")
        self.assertEqual(x["pr_ci"]["run_id"], 39776896152)
        self.assertEqual(x["pr_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(x["pr_ci"]["handoff_tests"], 66)
        self.assertEqual(x["main_ci"], {"run_id": 39778720560, "conclusion": "SUCCESS"})
        self.assertEqual(self.data["post_pr131_normalization"]["main_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        observed = self.data["post_pr131_postmain_terminal_observation"]
        self.assertEqual(observed["run_id"], 39776433056)
        self.assertEqual(observed["conclusion"], "SUCCESS")
        self.assertEqual(observed["merge_sha"], "37d8aa100e9d6fe61bbe6650f554a147661e703e")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertIn("PR #132", self.doc)

    def test_68_owner_reported_fileid_metadata_never_proves_absence_of_writer(self):
        x = self.data["g2b_owner_reported_oct22"]
        self.assertEqual(x["kind"], "OWNER_REPORTED_SANITIZED_STDOUT_NOT_INDEPENDENTLY_ATTESTED")
        self.assertEqual([a["name"] for a in x["observations"]],
                         ["DISCOVERY", "MARKER", "METADATA", "WIN32_FILE_ID"])
        self.assertEqual(x["observations"][0]["restored_candidates"], 1)
        self.assertEqual(x["observations"][1]["selected_db_sidecars_seen"], 0)
        self.assertEqual(x["observations"][2]["two_sample_stability"], "PASS")
        self.assertEqual(x["observations"][3]["two_handle_identity"], "STABLE")
        self.assertEqual(x["observations"][3]["share_mode"], "FILE_SHARE_READ|WRITE|DELETE")
        self.assertFalse(x["strong_historic_source_authentication"])
        self.assertFalse(x["header_or_sql_version_verified"])
        self.assertFalse(x["original_sqlite_opened"])
        self.assertEqual(x["continuous_writer_exclusion"], "NOT_PROVEN")
        self.assertEqual(x["global_g2b_acceptance"], "NOT_ACCEPTED")
        self.assertEqual(x["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(x["operator_paths_published"])
        self.assertEqual(x["original_files_in_ci"], "NONE")
        q = self.data["m3_2_product_progress"]["test_only_g2b_win32_share_all_writer_counterexample"]
        self.assertEqual(q["test_count"], 8)
        self.assertEqual(q["windows_toy_count"], 4)
        self.assertEqual(q["pure_refusal_count"], 4)
        self.assertEqual(q["writer_absence"], "NOT_PROVEN")
        self.assertEqual(q["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(q["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(q["real_g3_authorized"])
        for name in ("doc", "tests", "workflow"):
            self.assertTrue((ROOT / q[name]).is_file())
        source = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn('GITHUB_ACTIONS', source)
        self.assertIn('tempfile.TemporaryDirectory', source)
        self.assertIn('SHARE_ALL = SHARE_READ | SHARE_WRITE | SHARE_DELETE', source)
        self.assertIn('TOY_BYTES_AFTER', source)
        self.assertNotIn('LOCALAPPDATA', source)
        self.assertNotIn('sqlite3.connect', source)
        self.assertEqual(q["first_ci"]["run_id"], 39835364262)
        self.assertEqual(q["first_ci"]["conclusion"], "FAILURE")
        self.assertEqual(q["corrected_test_08"],
                         "ATTRIBUTE_ONLY_SHARE_READ_DID_NOT_EXCLUDE_NEW_GENERIC_WRITE_IN_WINDOWS_CI_TOY")
        self.assertIn("G2B_WIN32_FILEID", self.doc)

    def test_69_pr133_win32_negative_proof_merge_never_promotes_operator(self):
        x = self.data["post_pr133_normalization"]
        self.assertEqual(x["merged_pr"], 133)
        self.assertEqual(x["merge_sha"], "604817c8457aaf7136f587aaaff28ff862e2702a")
        self.assertEqual(x["pr_head_sha"], "d2bf3134054c4f1a05432c51055134fec7b4a0b2")
        self.assertEqual(x["pr_ci"], {"run_id": 39835840939, "conclusion": "SUCCESS",
                                       "job_steps": 75, "g2b_counterexample_tests": 8,
                                       "handoff_tests": 68, "rust_tests": 132,
                                       "chromium_normal": 53, "chromium_strict_csp": 53})
        self.assertEqual(x["first_failed_ci"]["run_id"], 39835364262)
        self.assertEqual(x["first_failed_ci"]["conclusion"], "FAILURE")
        self.assertEqual(x["main_ci"], {"run_id": 39837202639,
                                         "conclusion": "IN_PROGRESS_AT_CHECKPOINT"})
        self.assertEqual(x["source_identity"], "PARTIAL_LOCAL_IDENTITY_ONLY")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_global"], "NOT_ACCEPTED")
        self.assertEqual(x["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertFalse(x["operator_paths_published"])
        toy = self.data["m3_2_product_progress"]["test_only_g2b_win32_share_all_writer_counterexample"]
        self.assertEqual(toy["status"], "SOURCE_MERGED_WINDOWS_CI_QUALIFIED_TOY_ONLY_NOT_OPERATOR")
        self.assertEqual(toy["corrected_ci"]["run_id"], 39835840939)
        self.assertEqual(toy["corrected_ci"]["conclusion"], "SUCCESS")
        self.assertFalse(toy["fileid_stability_proves_writer_absence"])
        self.assertFalse(toy["attribute_only_share_read_excludes_writer"])
        self.assertEqual(toy["operator_authority"], "NONE")
        self.assertIn("PR #133", self.doc)

    def test_70_pr134_terminal_documentary_merge_and_evidence_boundary(self):
        x = self.data["post_pr134_normalization"]
        self.assertEqual(x["merged_pr"], 134)
        self.assertEqual(x["merge_sha"], "a1185b8345999f10814fd54dab96890f70236a5c")
        self.assertEqual(x["pr_head_sha"], "f0db9b28d0e8492f3bc64c952b722873ae61311e")
        self.assertEqual(x["pr_ci"], {"run_id": 39837909918, "conclusion": "SUCCESS",
                                       "job_steps": 75, "handoff_tests": 69,
                                       "rust_tests": 132, "chromium_normal": 53,
                                       "chromium_strict_csp": 53})
        self.assertEqual(x["main_ci"], {"run_id": 39839580270, "conclusion": "SUCCESS", "job_steps": 75})
        self.assertEqual(self.data["post_pr133_normalization"]["main_ci"]["conclusion"],
                         "IN_PROGRESS_AT_CHECKPOINT")
        self.assertTrue(x["preserve_pr133_pending_snapshot"])
        later = self.data["post_pr133_postmain_terminal_observation"]
        self.assertEqual(later["run_id"], 39837202639)
        self.assertEqual(later["conclusion"], "SUCCESS")
        self.assertEqual(later["merge_sha"], "604817c8457aaf7136f587aaaff28ff862e2702a")
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_global"], "NOT_ACCEPTED")
        self.assertEqual(x["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        evidence = self.data["m3_2_g2b_g3_evidence_decision"]
        self.assertEqual(evidence["kind"], "SOURCE_ONLY_DECISION_NO_OPERATOR_AUTHORIZATION")
        self.assertTrue((ROOT / evidence["document"]).is_file())
        review = (ROOT / evidence["document"]).read_text(encoding="utf-8")
        for phrase in ("NO REAL DATABASE ACCESS", "NOT PROVEN",
                       "STOP_UNAVAILABLE", "Online Backup", "FILE_READ_ATTRIBUTES"):
            self.assertIn(phrase, review)
        self.assertEqual(evidence["trusted_owner_connection"], "NOT_PROVEN_OR_AVAILABLE")
        self.assertEqual(evidence["safe_cold_source"], "NOT_PROVEN")
        self.assertFalse(evidence["fileid_stability_proves_writer_absence"])
        self.assertTrue(evidence["online_backup_requires_authenticated_owner"])
        self.assertFalse(evidence["online_backup_source_lock_continuous"])
        self.assertFalse(evidence["raw_copy_allowed"])
        self.assertFalse(evidence["read_only_uri_sufficient"])
        self.assertTrue(evidence["third_location_required"])
        self.assertEqual(evidence["real_operator_execution"], "NONE")
        self.assertEqual(evidence["original_db_opened"], "NONE")
        self.assertEqual(evidence["g2b_global"], "NOT_ACCEPTED")
        self.assertEqual(evidence["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(evidence["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(evidence["product"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertIn("PR #134", self.doc)

    def test_71_pr135_merge_terminal_and_resume_prompt_no_real_authority(self):
        x = self.data["post_pr135_normalization"]
        self.assertEqual(x["merged_pr"], 135)
        self.assertEqual(x["merge_sha"], "b54f4111eed020c80a70f91bd3e15b544f842545")
        self.assertEqual(x["pr_head_sha"], "acb901bd1844d93ea0562415a7438a4b21e7f4b8")
        self.assertEqual(x["pr_ci"], {"run_id": 39841578935, "conclusion": "SUCCESS",
                                       "job_steps": 75, "handoff_tests": 70,
                                       "rust_tests": 132, "chromium_normal": 53,
                                       "chromium_strict_csp": 53})
        self.assertEqual(x["main_ci"], {"run_id": 39843166291, "conclusion": "SUCCESS",
                                         "job_steps": 75})
        self.assertEqual(self.data["post_pr134_normalization"]["main_ci"]["conclusion"], "SUCCESS")
        self.assertTrue(x["historic_snapshots_preserved"])
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_global"], "NOT_ACCEPTED")
        self.assertEqual(x["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(x["g2b_to_g6"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["real_sqlite_access"], "NONE")
        self.assertEqual(x["tauri_writer_ipc"], "NONE")
        self.assertEqual(x["runtime_app_mount"], "NONE")
        self.assertEqual(x["pr35_state"], "OPEN_DRAFT")
        prompt = (ROOT / "docs/continuity/RESUME_PROMPT.md").read_text(encoding="utf-8")
        for phrase in ("PR #135", "39843166291", "PR #136",
                       "IN_PROGRESS_NOT_ACCEPTED", "STOP_UNAVAILABLE",
                       "ne jamais", "parallèle"):
            self.assertIn(phrase, prompt)
        self.assertIn("PR #135", self.doc)

    def test_72_pr136_terminal_and_stale_lease_toy_never_authorizes_originals(self):
        x = self.data["post_pr136_normalization"]
        self.assertEqual(x["merged_pr"], 136)
        self.assertEqual(x["merge_sha"], "d4837f1b292f37ec4b87926bc79a7c1c999d1fbe")
        self.assertEqual(x["pr_head_sha"], "ea94377a80001fbd701ec06c7a84b7cba5b95036")
        self.assertEqual(x["pr_ci"], {"run_id": 39848398829, "conclusion": "SUCCESS",
                                       "job_steps": 75, "handoff_tests": 71,
                                       "rust_tests": 132, "chromium_normal": 53,
                                       "chromium_strict_csp": 53})
        self.assertEqual(x["main_ci"], {"run_id": 39849940959, "conclusion": "SUCCESS",
                                         "job_steps": 75})
        self.assertEqual(self.data["post_pr135_normalization"]["main_ci"]["conclusion"], "SUCCESS")
        self.assertTrue(x["historic_snapshots_preserved"])
        self.assertEqual(x["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(x["writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2b_global"], "NOT_ACCEPTED")
        self.assertEqual(x["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(x["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective"], "NOT_STARTED")
        self.assertEqual(x["operator_execution"], "NONE")
        self.assertEqual(x["original_sqlite_access"], "NONE")
        self.assertEqual(x["pr35_state"], "OPEN_DRAFT")

        toy = self.data["m3_2_product_progress"]["test_only_unmediated_writer_negative_witness"]
        self.assertEqual(toy["status"], "SOURCE_MERGED_WINDOWS_CI_QUALIFIED_RAM_TOY_ONLY_NOT_OPERATOR")
        self.assertEqual(toy["fixture"], "INVENTED_SQLITE_RAM_ONLY_NO_OPERATOR_FILE")
        self.assertFalse(toy["owner_token_proves_writer_exclusion"])
        self.assertFalse(toy["online_backup_proves_source_authentication"])
        self.assertEqual(toy["real_sqlite_access"], "NONE")
        self.assertEqual(toy["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(toy["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(toy["product_status"], "IN_PROGRESS_NOT_ACCEPTED")
        for name in ("document", "rust"):
            self.assertTrue((ROOT / toy[name]).is_file())
        rust = (ROOT / toy["rust"]).read_text(encoding="utf-8")
        self.assertIn("fn " + toy["test_name"] + "()", rust)
        self.assertIn('["Unmediated invented write"]', rust)
        self.assertIn("assert_eq!(owner.lease()?, old);", rust)
        self.assertIn("Connection::open_in_memory()", rust)
        self.assertNotIn("Connection::open(path)", rust)
        self.assertNotIn("#[tauri::command]", rust)
        prompt = (ROOT / "docs/continuity/RESUME_PROMPT.md").read_text(encoding="utf-8")
        for phrase in ("PR #136", "39849940959", "PR #137", "STOP_UNAVAILABLE"):
            self.assertIn(phrase, prompt)
        self.assertIn("PR #136", self.doc)

    def test_73_pr137_merge_and_all_writer_guard_do_not_promote_real_g3(self):
        x = self.data["post_pr137_normalization"]
        # Historical PR #147 evidence is stable even as the living handoff advances.
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 147)
        historic = self.data["post_pr147_terminal_observation"]
        self.assertEqual(historic["merge_sha"], "7e67c5daf98821700f176965dadd52bafd0064fa")
        self.assertEqual(historic["source_sha"], "472c13344c2d6fe7c75c1812acf05f3236799e65")
        self.assertEqual(x["merged_pr"], 137)
        self.assertEqual(x["merge_sha"], "4d5a2bcb68dd439fac1846d354f3f808138457f1")
        self.assertEqual(x["pr_head_sha"], "892a42e9ea0c84ab9af9fb45536d502d99252155")
        self.assertEqual(x["pr_ci"], {"run_id": 39876891920, "conclusion": "SUCCESS",
                                       "job_steps": 75, "handoff_tests": 72,
                                       "rust_tests": 132, "chromium_normal": 53,
                                       "chromium_strict_csp": 53,
                                       "ram_unmediated_negative": "PASS"})
        self.assertEqual(x["old_sha_ci"]["qualification_for_merge"],
                         "INVALIDATED_BY_NEW_COMMIT")
        self.assertEqual(x["main_ci"], {"run_id": 39900039763,
                                         "conclusion": "IN_PROGRESS_AT_CHECKPOINT"})
        self.assertEqual(self.data["main_ci_post_merge"]["sha"], x["merge_sha"])
        self.assertEqual(self.data["main_ci_post_merge"]["conclusion"],
                         "IN_PROGRESS_AT_CHECKPOINT")
        for key, expected in {"writer_absence": "NOT_PROVEN",
                              "g2b_global": "NOT_ACCEPTED",
                              "g2c": "NOT_AUTHORIZED",
                              "real_g3": "STOP_UNAVAILABLE",
                              "product_status": "IN_PROGRESS_NOT_ACCEPTED",
                              "historical": "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                              "prospective": "NOT_STARTED",
                              "original_sqlite_access": "NONE",
                              "operator_execution": "NONE",
                              "pr35_state": "OPEN_DRAFT"}.items():
            self.assertEqual(x[key], expected)

        gate = self.data["m3_2_product_progress"]["test_only_owner_writer_channels_guard"]
        self.assertEqual(gate["field"], "all_mutation_entrypoints_mediated")
        self.assertFalse(gate["default"])
        self.assertEqual(gate["synthetic_tests_added"], 3)
        self.assertFalse(gate["actual_all_writers_verified"])
        self.assertFalse(gate["real_g3_authorized"])
        self.assertEqual(gate["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(gate["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(gate["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(gate["operator_file_access"], "NONE")
        for name in ("code", "tests", "doc"):
            self.assertTrue((ROOT / gate[name]).is_file())
        policy = (ROOT / gate["code"]).read_text(encoding="utf-8")
        test_source = (ROOT / gate["tests"]).read_text(encoding="utf-8")
        self.assertIn("all_mutation_entrypoints_mediated: bool = False", policy)
        self.assertIn('"all_mutation_entrypoints_mediated"', policy)
        self.assertIn("test_unmediated_writer_veto_even_if_owner_mutex_is_serialized",
                      test_source)
        prompt = (ROOT / "docs/continuity/RESUME_PROMPT.md").read_text(encoding="utf-8")
        for phrase in ("PR #137", "PR #138", "39900039763",
                       "IN_PROGRESS_NOT_ACCEPTED", "STOP_UNAVAILABLE"):
            self.assertIn(phrase, prompt)

    def test_74_pr138_terminal_is_separate_from_historic_checkpoints(self):
        current = self.data["post_pr138_terminal_observation"]
        self.assertEqual(current["pr"], 138)
        self.assertTrue(current["merged"])
        self.assertEqual(current["source_sha"], "29e662e2b27307bdae0a0107e02a6f1ae1fc59b7")
        self.assertEqual(current["source_ci"]["run_id"], 39900743598)
        self.assertEqual(current["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(current["merge_sha"], "78050c11b882ec852d8f211cedf3980166f30e9a")
        self.assertEqual(current["postmain_ci"]["run_id"], 39902762331)
        self.assertEqual(current["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(current["obsolete_run"]["qualification_for_final_head"], "INVALID")
        self.assertFalse(current["all_mutation_entrypoints_mediated_default"])
        self.assertFalse(current["real_writer_inventory_proven"])
        self.assertFalse(current["real_g3_authorized"])
        self.assertEqual(current["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(current["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(current["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(self.data["post_pr137_normalization"]["main_ci"]["conclusion"],
                         "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(self.data["main_ci_post_merge"]["conclusion"],
                         "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(self.data["post_pr137_postmain_terminal_observation"]["conclusion"],
                         "SUCCESS")
        for path in ("HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "RESUME_PROMPT.md", "README.md"):
            doc = (DIRECTORY / path).read_text(encoding="utf-8")
            self.assertIn("39902762331", doc, path)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", doc, path)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39902762331", roadmap)
        self.assertIn("IN_PROGRESS_NOT_ACCEPTED", roadmap)

    def test_75_pr139_terminal_and_trigger_candidate_do_not_promote_g3(self):
        p = self.data["post_pr139_terminal_observation"]
        self.assertEqual(p["pr"], 139)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "f9d28610bac2a97f517a39e9bceb5b0b4d85a96e")
        self.assertEqual(p["source_ci"]["run_id"], 39915173862)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["source_ci"]["handoff_tests"], 74)
        self.assertEqual(p["merge_sha"], "26e533c97d34ae36d25226730c7f74a7f0ee2e3f")
        self.assertEqual(p["postmain_ci"]["conclusion"], "QUEUED_AT_CHECKPOINT")
        self.assertTrue(p["historical_snapshots_preserved"])
        t = self.data["m3_2_product_progress"]["test_only_indirect_trigger_writer_negative"]
        self.assertEqual(t["ci"], "NEW_EXACT_HEAD_REQUIRED")
        self.assertFalse(t["proof_of_real_writer_mediation"])
        self.assertFalse(t["real_g3_authorized"])
        self.assertEqual(t["g3"], "STOP_UNAVAILABLE")
        self.assertEqual(t["writer_absence"], "NOT_PROVEN")
        source = (ROOT / t["rust_path"]).read_text(encoding="utf-8")
        self.assertIn(t["rust_test"], source)
        self.assertIn("CREATE TRIGGER invented_indirect_update", source)
        self.assertIn("Connection::open_in_memory()", source)
        witness = (ROOT / t["documentation"]).read_text(encoding="utf-8")
        self.assertIn("TEST-ONLY", witness)
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)", witness)
        self.assertEqual(self.data["post_pr138_terminal_observation"]["merge_sha"],
                         "78050c11b882ec852d8f211cedf3980166f30e9a")
        for name in ("HANDOFF_CURRENT.md", "RESUME_PROMPT.md", "NEXT.md",
                     "STATE.md", "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39915173862", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)

    def test_76_pr140_merge_and_data_version_ram_witness_do_not_grant_real_g3(self):
        p = self.data["post_pr140_terminal_observation"]
        self.assertEqual(p["pr"], 140)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "9d859cb5b61f87782cede0db1c9e59a3a113948d")
        self.assertEqual(p["source_ci"]["run_id"], 39917211662)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["source_ci"]["handoff_tests"], 75)
        self.assertEqual(p["merge_sha"], "f5a255e6687c68c1e6095d8e3a8c20277415741c")
        self.assertEqual(p["postmain_ci"]["conclusion"], "IN_PROGRESS_AT_CHECKPOINT")
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(p["sqlite_writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["historic"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(self.data["post_pr139_terminal_observation"]["postmain_ci"]["conclusion"],
                         "QUEUED_AT_CHECKPOINT")
        self.assertEqual(self.data["post_pr139_postmain_terminal_observation"]["conclusion"],
                         "SUCCESS")
        toy = self.data["m3_2_product_progress"]["test_only_same_connection_data_version_negative"]
        self.assertEqual(toy["qualification"], "NEW_EXACT_HEAD_CI_REQUIRED")
        self.assertEqual(toy["pragma"], "data_version")
        self.assertFalse(toy["real_writer_exclusion_proven"])
        self.assertFalse(toy["real_g3_authorized"])
        self.assertEqual(toy["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(toy["g3"], "STOP_UNAVAILABLE")
        source = (ROOT / toy["rust_path"]).read_text(encoding="utf-8")
        self.assertIn(toy["rust_test"], source)
        self.assertIn("PRAGMA data_version", source)
        self.assertIn("Connection::open_in_memory()", source)
        witness = (ROOT / toy["documentation"]).read_text(encoding="utf-8")
        self.assertIn("STRICTLY TEST-ONLY", witness)
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)", witness)
        for name in ("HANDOFF_CURRENT.md", "RESUME_PROMPT.md", "NEXT.md",
                     "STATE.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md", "HANDOFF_HISTORY.md"):
            text = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39917211662", text, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", text, name)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39917211662", roadmap)

    def test_77_short_and_long_resume_policy_is_copy_ready_and_mandatory(self):
        short_file = DIRECTORY / "RESUME_PROMPT_SHORT.md"
        long_file = DIRECTORY / "RESUME_PROMPT.md"
        self.assertTrue(short_file.is_file())
        self.assertTrue(long_file.is_file())
        short = short_file.read_text(encoding="utf-8")
        detailed = long_file.read_text(encoding="utf-8")
        self.assertLess(len(short), 4200, "Short resume must remain copy-friendly")
        self.assertGreater(len(detailed), len(short))
        self.assertIn("RESUME_PROMPT.md", short)
        self.assertIn("HANDOFF_CURRENT.md", short)
        self.assertIn("HANDOFF_CURRENT.json", short)
        self.assertIn("ROADMAP_STATUS_CURRENT.md", short)
        self.assertIn("main=" + self.data["last_confirmed_main_before_handoff"], short)
        self.assertIn("IN_PROGRESS_AT_CHECKPOINT", detailed)
        for status in ("IN_PROGRESS_NOT_ACCEPTED", "NOT_PROVEN", "STOP_UNAVAILABLE",
                       "PENDING_EXTERNAL_ATTESTATION(21/3/2)", "expected_head_sha"):
            self.assertIn(status, short)
            self.assertIn(status, detailed)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md"):
            self.assertIn(filename, self.policy)
            self.assertIn(filename, self.index)
        policy = self.data["resume_prompts_policy"]
        self.assertEqual(policy["short_path"], "docs/continuity/RESUME_PROMPT_SHORT.md")
        self.assertEqual(policy["long_path"], "docs/continuity/RESUME_PROMPT.md")
        self.assertEqual(policy["update_required"], "BOTH_FILES_IN_EVERY_FUTURE_PR")
        self.assertFalse(policy["real_g3_authorized"])
        ci = (ROOT / policy["diff_guard"]).read_text(encoding="utf-8")
        validator = (ROOT / "tools/m32_resume_pr_diff_policy.py").read_text(encoding="utf-8")
        self.assertIn("python tools/m32_resume_pr_diff_policy.py", ci)
        self.assertIn("M32_BOTH_RESUME_PROMPTS_EVERY_PR_PASS", validator)
        self.assertIn("STOP missing required resume prompt in this PR", validator)
        self.assertIn('"docs/continuity/RESUME_PROMPT_SHORT.md"', validator)
        self.assertIn('"docs/continuity/RESUME_PROMPT.md"', validator)
        self.assertIn("if: github.event_name == 'pull_request'", ci)

    def test_78_pr142_terminal_short_resume_and_negative_guard_do_not_promote_g3(self):
        p = self.data["post_pr142_terminal_observation"]
        self.assertEqual(p["pr"], 142)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "f17a5c62fb6cc5fcb6259138b4f529b8f07bc581")
        self.assertEqual(p["source_ci"]["run_id"], 39930833733)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["source_ci"]["handoff_tests"], 77)
        self.assertEqual(p["merge_sha"], "98216aa5f5045d6faa4202b76709507b61027534")
        self.assertEqual(p["postmain_ci"]["run_id"], 39932102283)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["product"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["real_g3_authorized"])
        self.assertEqual(self.data["resume_prompts_policy"]["kind"],
                         "PENDING_OWN_EXACT_SHA_CI_AND_PROTECTED_MERGE")
        q = self.data["resume_pr_diff_policy_negative_matrix"]
        self.assertEqual(q["test_cases"], 12)
        self.assertTrue(q["both_prompts_every_pr"])
        self.assertTrue(q["material_handoffs"])
        self.assertFalse(q["real_g3_authorized"])
        for key in ("code", "tests", "doc"):
            self.assertTrue((ROOT / q[key]).is_file(), q[key])
        # The short resume MUST stay focused on the latest verified checkpoint;
        # historical PR #142 CI belongs to the long resume and history, not the short.
        detailed = (DIRECTORY / "RESUME_PROMPT.md").read_text(encoding="utf-8")
        self.assertIn("39932102283", detailed)
        for filename in ("HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "NEXT.md",
                         "STATE.md", "M3_2_GATE_DECISION_CURRENT.md",
                         "RESUME_PROMPT.md", "README.md"):
            value = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("39932102283", value, filename)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39932102283", roadmap)

    def test_79_pr143_terminal_and_two_universes_candidate_not_authorized(self):
        p = self.data["post_pr143_terminal_observation"]
        self.assertTrue(p["merged"])
        self.assertEqual(p["pr"], 143)
        self.assertEqual(p["source_sha"], "61ae15427863ccaae7f2cd8a5b8ea6ff04c83f4c")
        self.assertEqual(p["source_ci"]["run_id"], 39935643729)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["merge_sha"], "cf90661173e9e6ed8d29caa181557b04e2d6fb63")
        self.assertEqual(p["postmain_ci"]["run_id"], 39936839961)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertFalse(p["real_g3_authorized"])
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["two_universe_fictional_browser_only_candidate"]
        self.assertEqual(q["scenarios"], 14)
        self.assertFalse(q["operator_windows_acceptance"])
        self.assertFalse(q["real_g3_authorized"])
        self.assertEqual(q["integration_with_app"], "NONE")
        for key in ("component", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file())
        component = (ROOT / q["component"]).read_text(encoding="utf-8")
        self.assertIn("inspectFictionalDraft(left)", component)
        self.assertIn("inspectFictionalDraft(right)", component)
        self.assertNotIn('from "./App"', component)
        self.assertNotIn("invoke(", component)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("14 read-only preview rejects", tests)
        self.assertIn("fiction-alpha", tests)
        self.assertIn("fiction-beta", tests)
        for name in ("README.md", "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md",
                     "NEXT.md", "STATE.md", "M3_2_GATE_DECISION_CURRENT.md",
                     "RESUME_PROMPT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39936839961", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        status = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39936839961", status)

    def test_80_pr144_postmain_success_and_manual_event_candidate_still_real_stop(self):
        p = self.data["post_pr144_terminal_observation"]
        self.assertEqual(p["pr"], 144)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "48b1e873292b4f65de90fbe128f76f0b5759d4db")
        self.assertEqual(p["source_ci"]["run_id"], 39940937603)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["merge_sha"], "c969f2c29e168e99e24d675c25a3217e789c9e2d")
        self.assertEqual(p["postmain_ci"]["run_id"], 39942208143)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["g3_real"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["fictional_manual_event_notebook_candidate"]
        self.assertEqual(q["scenarios"], 15)
        self.assertFalse(q["persisted"])
        self.assertFalse(q["app_mounted"])
        self.assertFalse(q["real_g3_authorized"])
        for name in ("model", "preview", "tests", "documentation"):
            self.assertTrue((ROOT / q[name]).is_file(), q[name])
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("withdrawFictionalEvent", model)
        self.assertIn("inspectFictionalDraft", model)
        self.assertNotIn("invoke(", model)
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39942208143", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39942208143", roadmap)

    def test_81_pr145_postmain_terminal_and_new_fictional_form_are_non_authorizing(self):
        p = self.data["post_pr145_terminal_observation"]
        self.assertEqual(p["pr"], 145)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "8151f1720c0e657fe66a191c21dafc084449486a")
        self.assertEqual(p["source_ci"]["run_id"], 39945373971)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["merge_sha"], "26987ffaf6ec7c1a02bca8c288243a3da2092469")
        self.assertEqual(p["postmain_ci"]["run_id"], 39946911406)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["product"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(p["writer_absence"], "NOT_PROVEN")
        q = self.data["m3_2_product_progress"]["fictional_manual_event_workshop_candidate"]
        self.assertEqual(q["scenarios"], 18)
        self.assertFalse(q["mounted_in_app"])
        self.assertFalse(q["windows_operator_acceptance"])
        self.assertFalse(q["real_g3_authorized"])
        for key in ("component", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        source = (ROOT / q["component"]).read_text(encoding="utf-8")
        self.assertIn("applyFictionalWorkshopAction", source)
        self.assertIn("useState", source)
        self.assertNotIn("invoke(", source)
        self.assertNotIn("localStorage.", source)
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        self.assertNotIn("M32FictionalEventManualWorkshop", app)
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            content = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39946911406", content, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", content, name)
        self.assertIn("39946911406",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_82_pr146_terminal_and_new_chromium_form_fictional_only(self):
        p = self.data["post_pr146_terminal_observation"]
        self.assertTrue(p["merged"])
        self.assertEqual(p["pr"], 146)
        self.assertEqual(p["source_sha"], "5959ca0fe3d4cfd29ec3b558c55c1e64c620594e")
        self.assertEqual(p["source_ci"]["run_id"], 39965156053)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["merge_sha"], "c451cc0b09e24242ecb1ea7cf5c488d1217b51ca")
        self.assertEqual(p["postmain_ci"]["run_id"], 39966405809)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        t = self.data["m3_2_product_progress"]["fictional_event_real_chromium_candidate"]
        self.assertEqual(t["added_browser_scenarios"], 9)
        self.assertEqual(t["browser_scenarios_per_mode"], 62)
        self.assertFalse(t["mounted_in_app"])
        self.assertFalse(t["windows_operator_acceptance"])
        for k in ("documentation", "browser", "fixture_stage"):
            self.assertTrue((ROOT / t[k]).is_file(), k)
        browser = (ROOT / t["browser"]).read_text(encoding="utf-8")
        self.assertIn("62-fictional-event-cycle-is-rejected", browser)
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 62/62", browser)
        stage = (ROOT / t["fixture_stage"]).read_text(encoding="utf-8")
        self.assertIn('"src/M32FictionalEventManualWorkshop.tsx"', stage)
        self.assertIn('"src/m32FictionalEventNotebook.ts"', stage)
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        self.assertNotIn("M32FictionalEventManualWorkshop", app)
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            current = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39966405809", current, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", current, name)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39966405809", roadmap)

    def test_83_pr147_terminal_and_structural_event_audit_candidate_no_real_g3(self):
        p = self.data["post_pr147_terminal_observation"]
        self.assertEqual(p["pr"], 147)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "472c13344c2d6fe7c75c1812acf05f3236799e65")
        self.assertEqual(p["source_ci"]["run_id"], 39979848160)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["merge_sha"], "7e67c5daf98821700f176965dadd52bafd0064fa")
        self.assertEqual(p["postmain_ci"]["run_id"], 39981173101)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["source_ci"]["chromium_normal"], 62)
        self.assertEqual(p["postmain_ci"]["chromium_strict_csp"], 62)
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["protected_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["fictional_event_audit_lineage_candidate"]
        self.assertEqual(q["added_cases"], 12)
        self.assertTrue(q["structural_only"])
        self.assertTrue(q["does_not_authenticate_history"])
        self.assertFalse(q["real_g3_authorized"])
        for name in ("model", "tests", "documentation"):
            self.assertTrue((ROOT / q[name]).is_file(), q[name])
        source = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("audit incomplet ou surnuméraire", source)
        self.assertIn("audit fictif absent, désordonné ou incompatible", source)
        self.assertNotIn("invoke(", source)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("27 rejects unexplained audit", tests)
        # The short prompt contains only the latest checkpoint, unlike the long/history.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39981173101", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        self.assertIn("39981173101",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_24_policy_requires_refetch_and_same_pr_handoff(self):
        for clause in ("Re-fetch", "HANDOFF_CURRENT.md", "HANDOFF_CURRENT.json",
                       "expected_head_sha", "autorisation"):
            self.assertIn(clause, self.policy)

    def test_84_pr148_terminal_and_fictional_tombstone_guard(self):
        p = self.data["post_pr148_terminal_observation"]
        self.assertEqual(p["pr"], 148)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "f4ff680ef82d91e2b10fe7ea9701e90d073453b4")
        self.assertEqual(p["source_ci"]["run_id"], 39985794291)
        self.assertEqual(p["source_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["merge_sha"], "4a8d09d99c1b2b2eb716b17acf733981c51ac340")
        self.assertEqual(p["postmain_ci"]["run_id"], 39987313809)
        self.assertEqual(p["postmain_ci"]["conclusion"], "SUCCESS")
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["fictional_event_withdrawal_tombstone_candidate"]
        self.assertEqual(q["added_tests"], 5)
        self.assertFalse(q["real_g3_authorized"])
        for k in ("model", "tests", "documentation"):
            self.assertTrue((ROOT / q[k]).is_file(), q[k])
        source = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("retrait sans version précédente", source)
        self.assertIn("pierre tombale modifiant la version précédente", source)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("32 accepts legitimate amend then withdraw", tests)
        # Short prompt is intentionally current-only; long/history retain PR148 CI.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39987313809", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("39987313809", roadmap)

    def test_85_pr149_terminal_and_fictional_runtime_shape_denials(self):
        p = self.data["post_pr149_terminal_observation"]
        self.assertTrue(p["merged"])
        self.assertEqual(p["pr"], 149)
        self.assertEqual(p["source_sha"], "6c040d264035bf1c92d256b58459382b5d7faa10")
        self.assertEqual(p["source_ci"], {"run_id": 39994596525, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "77e253193cae3d29ae164875c65be1bf3186f4ad")
        self.assertEqual(p["postmain_ci"], {"run_id": 39996127567, "conclusion": "SUCCESS"})
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["original_sqlite_touched"])
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 149)
        q = self.data["m3_2_product_progress"]["fictional_runtime_shape_denial_candidate"]
        self.assertEqual(q["new_tests"], 9)
        self.assertFalse(q["real_g3_authorized"])
        for key in ("model", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn('typeof event.event_id !== "string"', model)
        self.assertIn('Array.isArray(audit)', model)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("41 preserves legitimate interleaved", tests)
        # The short prompt is current-only, older terminal CI remains in full handoff.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            data = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("39996127567", data, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", data, name)
        self.assertIn("39996127567",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_86_pr150_terminal_and_readonly_fictional_event_history(self):
        p = self.data["post_pr150_terminal_observation"]
        self.assertEqual(p["pr"], 150)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "b39506bce112b828477d9c4b1d1f14076dc3fb38")
        self.assertEqual(p["source_ci"], {"run_id": 40006337923, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "20658fdc87fd8deca712611f74f4e9cdf1389807")
        self.assertEqual(p["postmain_ci"], {"run_id": 40007837202, "conclusion": "SUCCESS"})
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["original_sqlite_touched"])
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 150)
        q = self.data["m3_2_product_progress"]["fictional_event_readonly_history_candidate"]
        self.assertEqual(q["new_tests"], 8)
        self.assertTrue(q["source_only"])
        self.assertFalse(q["real_g3_authorized"])
        for key in ("model", "preview", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("auditedFictionalEventHistory", model)
        self.assertIn("Object.freeze", model)
        preview = (ROOT / q["preview"]).read_text(encoding="utf-8")
        self.assertIn('aria-label="Historique des versions fictives"', preview)
        self.assertIn("<details>", preview)
        self.assertNotIn("invoke(", model + preview)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("49 renders a withdrawn event", tests)
        # The short prompt is intentionally current-only; PR150 remains in full history.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40007837202", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("40007837202", roadmap)

    def test_87_pr151_terminal_and_fictional_version_deltas(self):
        p = self.data["post_pr151_terminal_observation"]
        self.assertEqual(p["pr"], 151)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "ab0ffd3e1c0d08cb57325a2f5ef91c1967616716")
        self.assertEqual(p["initial_source_ci"], {
            "run_id": 40010433915, "conclusion": "FAILURE",
            "cause": "HISTORIC_HANDOFF_ASSERTION_EQUAL_149"})
        self.assertEqual(p["source_ci"], {"run_id": 40010733862, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "2e0b29bfc2d2698a636f4adc41d5b4e5a87c3ece")
        self.assertEqual(p["postmain_ci"], {"run_id": 40012175419, "conclusion": "SUCCESS"})
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 151)
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["original_sqlite_touched"])
        q = self.data["m3_2_product_progress"]["fictional_event_version_delta_candidate"]
        self.assertEqual(q["new_tests"], 8)
        self.assertTrue(q["source_only"])
        self.assertFalse(q["real_g3_authorized"])
        for key in ("model", "preview", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("changed_fields", model)
        self.assertIn("Object.freeze(changedFields)", model)
        preview = (ROOT / q["preview"]).read_text(encoding="utf-8")
        self.assertIn("modifications de contenu", preview)
        self.assertIn("<details>", preview)
        self.assertNotIn("invoke(", model + preview)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("57 renders accessible version differences", tests)
        # The short prompt is current-only; keep PR151 source/postmain CI in full history.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40012175419", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        self.assertIn("40012175419",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_88_pr152_terminal_and_fictional_before_after_preview(self):
        p = self.data["post_pr152_terminal_observation"]
        self.assertTrue(p["merged"])
        self.assertEqual(p["pr"], 152)
        self.assertEqual(p["source_sha"], "840c09535b6566b6738ea21d498ec347d2a76e44")
        self.assertEqual(p["initial_source_ci"], {
            "run_id": 40014673844, "conclusion": "FAILURE",
            "cause": "HISTORIC_PR150_CI_IN_SHORT_PROMPT"})
        self.assertEqual(p["source_ci"], {"run_id": 40014823165, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "5346ddb76fadfd3e2cec687522c41bf94bfedec9")
        self.assertEqual(p["postmain_ci"], {"run_id": 40016058394, "conclusion": "SUCCESS"})
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 152)
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["original_sqlite_touched"])
        q = self.data["m3_2_product_progress"]["fictional_event_before_after_candidate"]
        self.assertEqual(q["new_tests"], 8)
        self.assertTrue(q["source_only"])
        self.assertFalse(q["real_g3_authorized"])
        for key in ("model", "preview", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("field_differences", model)
        self.assertIn("Object.freeze(fieldDifferences)", model)
        preview = (ROOT / q["preview"]).read_text(encoding="utf-8")
        self.assertIn("Valeurs avant et après fictives", preview)
        self.assertIn('diff.before === null', preview)
        self.assertNotIn("invoke(", model + preview)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("65 renders explicit before-after", tests)
        # Only current checkpoint belongs to SHORT. The full documents hold history.
        # SHORT is current-only. Old PR152 exact CI is retained in detailed history.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40016058394", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        self.assertIn("40016058394",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_89_pr153_terminal_and_explicit_selected_fictional_event_comparison(self):
        p = self.data["post_pr153_terminal_observation"]
        self.assertEqual(p["pr"], 153)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "a211822c0618e68090633f874cde6b2c216204a8")
        self.assertEqual(p["source_ci"], {"run_id": 40020544737, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "c581ceb5056cb8e0d61646c02d3af722afb47a3e")
        self.assertEqual(p["postmain_ci"], {"run_id": 40021898423, "conclusion": "SUCCESS"})
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 153)
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["original_sqlite_touched"])
        q = self.data["m3_2_product_progress"]["fictional_event_selected_version_comparison_candidate"]
        self.assertEqual(q["new_tests"], 9)
        self.assertTrue(q["source_only"])
        self.assertFalse(q["real_g3_authorized"])
        self.assertFalse(q["no_persistence"] is False)
        for key in ("model", "preview", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        self.assertIn("compareFictionalEventVersions", model)
        self.assertIn("Object.freeze(differences)", model)
        self.assertIn("toVersion <= fromVersion", model)
        preview = (ROOT / q["preview"]).read_text(encoding="utf-8")
        self.assertIn("Comparaison cumulative des versions fictives", preview)
        self.assertIn("<details>", preview)
        self.assertNotIn("invoke(", model + preview)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("74 presents cumulative first-to-last", tests)
        # Short resume prompt is current-only. PR153 terminal CI stays in full history.
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40021898423", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        self.assertIn("40021898423",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_90_pr154_terminal_and_controlled_selected_fictional_preview(self):
        p = self.data["post_pr154_terminal_observation"]
        self.assertTrue(p["merged"])
        self.assertEqual(p["pr"], 154)
        self.assertEqual(p["source_sha"], "5d91e198e455c33a2782804310377f19ec746bee")
        self.assertEqual(p["source_ci"], {"run_id": 40025773741, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "391cc3972c87b7f3ae0fda033b55971f268d7fbe")
        self.assertEqual(p["postmain_ci"], {"run_id": 40027154468, "conclusion": "SUCCESS"})
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 154)
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["operator_windows_validation"])
        self.assertFalse(p["original_sqlite_touched"])
        q = self.data["m3_2_product_progress"]["fictional_controlled_preview_selection_candidate"]
        self.assertEqual(q["new_tests"], 9)
        self.assertTrue(q["source_only"])
        self.assertTrue(q["no_persistence"])
        self.assertFalse(q["real_g3_authorized"])
        self.assertTrue(q["not_mounted_in_application"])
        for key in ("model", "preview", "tests", "documentation"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        preview = (ROOT / q["preview"]).read_text(encoding="utf-8")
        self.assertIn("FictionalVersionPreviewSelection", preview)
        self.assertIn("Comparaison fictive demandée explicitement", preview)
        self.assertIn("compareFictionalEventVersions", preview)
        self.assertNotIn("invoke(", preview)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("83 compares a withdrawn tombstone", tests)
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md",
                     "NEXT.md", "STATE.md", "M3_2_GATE_DECISION_CURRENT.md"):
            body = (DIRECTORY / name).read_text(encoding="utf-8")
            # Historical source evidence belongs to the long handoff, not the current-only short prompt.
            self.assertIn("40027154468", body, name)
            self.assertIn("IN_PROGRESS_NOT_ACCEPTED", body, name)
        self.assertIn("40027154468",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_91_pr155_terminal_and_browser_only_version_pair_picker(self):
        p = self.data["post_pr155_terminal_observation"]
        self.assertEqual(p["pr"], 155)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "45b5febd3dbd594e28eab51bea62806ff3e43017")
        self.assertEqual(p["source_ci"], {"run_id": 40029859356, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "ccf5ba31b35c57b5ea572109e64015fdc1ca35cd")
        self.assertEqual(p["postmain_ci"], {"run_id": 40030841723, "conclusion": "SUCCESS"})
        self.assertEqual(p["event_tests"], 83)
        self.assertEqual(p["handoff_tests"], 90)
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        q = self.data["m3_2_product_progress"]["fictional_version_pair_picker_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertEqual(q["added_event_tests"], 4)
        self.assertEqual(q["added_browser_cases_per_mode"], 8)
        for key in ("component", "browser_lab", "tests", "qualification"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        src = (ROOT / q["component"]).read_text(encoding="utf-8")
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        self.assertIn("M32FictionalEventNotebookPreview", src)
        self.assertIn("auditedFictionalEventHistory", src)
        self.assertNotIn("M32FictionalEventVersionPairLab", app)
        for term in ("invoke(", "localStorage", "fetch(", "@tauri-apps"):
            self.assertNotIn(term, src)
        b = (ROOT / "tools/m32_browser_interaction.cjs").read_text(encoding="utf-8")
        self.assertIn("70-pair-picker-script-looking-label-inert", b)
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 70/70", b)
        stage = (ROOT / "tools/m32_ci_fixture_stage.cjs").read_text(encoding="utf-8")
        self.assertIn('"src/M32FictionalEventVersionPairLab.tsx"', stage)
        self.assertIn('"src/M32FictionalEventNotebookPreview.tsx"', stage)
        ts = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("87 escapes hostile-looking event labels", ts)
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40030841723", (DIRECTORY / name).read_text(encoding="utf-8"))
        self.assertIn("40030841723",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_92_pr156_terminal_and_live_fictional_workshop_comparison_candidate(self):
        p = self.data["post_pr156_terminal_observation"]
        self.assertEqual(p["pr"], 156)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "cb65a8c902146a7252e3682cf1f5f08f54e7f190")
        self.assertEqual(p["source_ci"], {"run_id": 40059088846, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "4de256f4666500e4fc9a9482e52c8116869a35ca")
        self.assertEqual(p["postmain_ci"], {"run_id": 40059860336, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 91)
        self.assertEqual(p["event_tests"], 87)
        self.assertEqual(p["chromium_normal"], 70)
        self.assertEqual(p["chromium_strict_csp"], 70)
        self.assertEqual(p["rust_tests"], 132)
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 156)
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(p["original_sqlite_touched"])
        q = self.data["m3_2_product_progress"]["fictional_live_workshop_comparison_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertEqual(q["added_event_tests"], 3)
        self.assertEqual(q["added_browser_cases_per_mode"], 6)
        self.assertFalse(q["mounted_in_application"])
        self.assertFalse(q["real_g3_authorized"])
        for field in ("workshop", "selector", "tests", "browser", "qualification"):
            self.assertTrue((ROOT / q[field]).is_file(), field)
        workshop = (ROOT / q["workshop"]).read_text(encoding="utf-8")
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        self.assertIn("M32FictionalEventVersionPairLab notebook={book}", workshop)
        self.assertIn("aria-expanded={compareOpen}", workshop)
        self.assertNotIn("M32FictionalEventManualWorkshop", app)
        # Reject executable persistent/network/IPC API use, not truthful comment text.
        self.assertNotRegex(workshop, r"\b(?:localStorage|sessionStorage)\s*(?:\.|\[)")
        self.assertNotRegex(workshop, r"\b(?:fetch|invoke)\s*\(")
        self.assertNotIn("@tauri-apps", workshop)
        browser = (ROOT / q["browser"]).read_text(encoding="utf-8")
        self.assertIn("76-live-workshop-comparison-escapes-user-looking-script", browser)
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 76/76", browser)
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        self.assertIn("90 refuses forged origin", tests)
        # Historical evidence persists in long documents; the short prompt tracks latest main.
        for name in ("RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "NEXT.md",
                     "STATE.md", "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40059860336", (DIRECTORY / name).read_text(encoding="utf-8"))
        self.assertIn("40059860336",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_93_pr157_terminal_accelerated_historical_copy_and_gate_choice(self):
        p = self.data["post_pr157_terminal_observation"]
        self.assertEqual(p["pr"], 157)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "956154c4be0645536d356a48c6d75d0bf92bdc37")
        self.assertEqual(p["source_ci"], {"run_id": 40061031363, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "645b50f438d12165d0eae46f1c3d586f07819480")
        self.assertEqual(p["postmain_ci"], {"run_id": 40061815168, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 92)
        self.assertEqual(p["event_tests"], 90)
        self.assertEqual(p["chromium_normal"], 76)
        self.assertEqual(p["chromium_strict_csp"], 76)
        self.assertEqual(p["rust_tests"], 132)
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 157)
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["fictional_historical_draft_copy_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertEqual(q["added_event_tests"], 6)
        self.assertEqual(q["added_browser_cases_per_mode"], 6)
        self.assertFalse(q["mounted_in_application"])
        self.assertFalse(q["real_g3_authorized"])
        for key in ("model", "workshop", "tests", "browser", "qualification", "acceleration"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        model = (ROOT / q["model"]).read_text(encoding="utf-8")
        ui = (ROOT / q["workshop"]).read_text(encoding="utf-8")
        tests = (ROOT / q["tests"]).read_text(encoding="utf-8")
        browser = (ROOT / q["browser"]).read_text(encoding="utf-8")
        app = (ROOT / "src/App.tsx").read_text(encoding="utf-8")
        self.assertIn("prepareFictionalEventHistoricalDraft(", model)
        self.assertIn("Object.freeze({", model)
        self.assertIn("setReason(\"\");", ui)
        self.assertIn("Préparer la correction depuis cette version", ui)
        self.assertIn("96 rejects a forged SQLite-origin notebook", tests)
        self.assertIn("82-historical-copy-renders-script-shaped-title-inert", browser)
        self.assertIn("M32_BROWSER_REAL_CHROMIUM_PASS 82/82", browser)
        self.assertNotIn("M32FictionalEventManualWorkshop", app)
        for source in (model, ui):
            self.assertNotRegex(source, r"\b(?:localStorage|sessionStorage)\s*(?:\.|\[)")
            self.assertNotRegex(source, r"\b(?:fetch|invoke)\s*\(")
            self.assertNotIn("@tauri-apps", source)
        decision = (ROOT / q["acceleration"]).read_text(encoding="utf-8")
        for term in ("pre_m24_early_manifest", "original_acls", "pre_repair_json",
                     "activation_marker", "isolated_v6", "PENDING_EXTERNAL_ATTESTATION",
                     "NOT_STARTED", "STOP_UNAVAILABLE", "AUCUNE AUTORISATION"):
            self.assertIn(term, decision)
        for name in ("RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "NEXT.md",
                     "STATE.md", "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40061815168", (DIRECTORY / name).read_text(encoding="utf-8"))
        self.assertIn("40061815168",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_94_pr158_terminal_and_early_typecheck_acceleration_candidate(self):
        p = self.data["post_pr158_terminal_observation"]
        self.assertEqual(p["pr"], 158)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "2543315b0b8ab9a17f3ac49b5d68c76717b0317f")
        self.assertEqual(p["source_ci"], {"run_id": 40063511352, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "fdae74efac90b35ffdc06110c6c9b4e14ce95b10")
        self.assertEqual(p["postmain_ci"], {"run_id": 40064299969, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 93)
        self.assertEqual(p["event_tests"], 96)
        self.assertEqual(p["chromium_normal"], 82)
        self.assertEqual(p["chromium_strict_csp"], 82)
        self.assertEqual(p["rust_tests"], 132)
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 158)
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["writer_absence"], "NOT_PROVEN")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["ci_early_typecheck_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertFalse(q["real_g3_authorized"])
        self.assertFalse(q["changes_protect_main"])
        self.assertEqual(q["extra_windows_steps"], 1)
        for key in ("workflow", "qualification", "test"):
            self.assertTrue((ROOT / q[key]).is_file(), key)
        workflow = (ROOT / q["workflow"]).read_text(encoding="utf-8")
        self.assertEqual(workflow.count("npx tsc --noEmit --pretty false"), 1)
        install = workflow.index("      - name: Install frontend dependencies from lockfile")
        early = workflow.index("      - name: Early frontend TypeScript typecheck (no emission)")
        chromium = workflow.index("      - name: M3.2 real Chromium synthetic-only UI interaction")
        build = workflow.index("      - name: Frontend production build")
        rust = workflow.index("      - name: Rust tests from lockfile")
        self.assertTrue(install < early < chromium < build < rust)
        for required in ("run: npm ci", "run: npm run test:ci",
                         "run: npm run build", "cargo test --manifest-path",
                         "M3.2 living handoff source-only contract checks",
                         "M3.2 require both resume prompts on every pull request",
                         "node tools/m32_browser_interaction.cjs",
                         "M3.2 G3 source identity SQLite Win32 shortcut refusal"):
            self.assertIn(required, workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("Swatinem/rust-cache", workflow)
        self.assertNotIn("actions/cache@", workflow)
        for name in ("RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "NEXT.md",
                     "STATE.md", "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40064299969",
                (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40064299969",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_95_pr159_terminal_and_real_vite_dependabot_security_lockfix_candidate(self):
        p = self.data["post_pr159_terminal_observation"]
        self.assertEqual(p["pr"], 159)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "4ed2e34426474b5baf945fbcbe42bc842d955eb8")
        self.assertEqual(p["source_ci"], {"run_id": 40067055296, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "3cbe793e4c6d7779802a2cba55640419599df1b3")
        self.assertEqual(p["postmain_ci"], {"run_id": 40067824098, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 94)
        self.assertEqual(p["event_tests"], 96)
        self.assertEqual(p["chromium_normal"], 82)
        self.assertEqual(p["chromium_strict_csp"], 82)
        self.assertEqual(p["rust_tests"], 132)
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 159)
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        q = self.data["m3_2_product_progress"]["npm_vite_dependabot_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertFalse(q["real_g3_authorized"])
        self.assertEqual(q["intended_fixed_npm_alerts"], 5)
        self.assertEqual(q["unresolved_rust_alerts"], 1)
        self.assertEqual(q["vulnerable_vite_version"], "8.0.16")
        self.assertEqual(q["patched_vite_version"], "8.1.6")
        for field in ("manifest", "lock", "cargo_lock", "qualification"):
            self.assertTrue((ROOT / q[field]).is_file(), field)
        pkg = json.loads((ROOT / q["manifest"]).read_text(encoding="utf-8"))
        npm_lock = json.loads((ROOT / q["lock"]).read_text(encoding="utf-8"))
        self.assertEqual(pkg["devDependencies"]["vite"], "8.1.6")
        self.assertEqual(npm_lock["packages"][""]["devDependencies"]["vite"], "8.1.6")
        self.assertEqual(npm_lock["packages"]["node_modules/vite"]["version"], "8.1.6")
        self.assertTrue(npm_lock["packages"]["node_modules/vite"]["integrity"].startswith("sha512-"))
        self.assertEqual(pkg["devDependencies"]["vitest"], "5.0.3")
        self.assertEqual(pkg["devDependencies"]["@tauri-apps/cli"], "2.12.1")
        self.assertNotIn("node_modules/launch-editor", npm_lock["packages"])
        workflow = (ROOT / ".github/workflows/m0-ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("TEMPORARY generate authenticated npm lock", workflow)
        self.assertNotIn("FABULAXIOM_LOCK_JSON", workflow)
        self.assertIn("run: npm ci", workflow)
        self.assertIn("npx tsc --noEmit --pretty false", workflow)
        self.assertIn("run: npm run build", workflow)
        self.assertIn("cargo test --manifest-path", workflow)
        self.assertIn("M3.2 real Chromium synthetic-only UI interaction", workflow)
        self.assertIn("Verify dependency locks are unchanged", workflow)
        cargo = (ROOT / q["cargo_lock"]).read_text(encoding="utf-8")
        self.assertIn('name = "glib"' + chr(10) + 'version = "0.18.5"', cargo)
        self.assertIn("GHSA-wrw7-89jp-8q8g",
            (ROOT / q["qualification"]).read_text(encoding="utf-8"))
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40067824098",
                (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40067824098",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_96_pr161_terminal_and_linux_glib_open_windows_target_audit_candidate(self):
        from m32_glib_target_audit import (CMD, GTK_PACKAGES, TRIPLE,
                                           graph_packages, assess_windows_graph,
                                           lock_glib_versions)
        p = self.data["post_pr161_terminal_observation"]
        self.assertEqual(p["pr"], 161)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "956c5a2cfa4239759e175429af34cab9753960a8")
        self.assertEqual(p["source_ci"], {"run_id": 40071869911, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "6cf1dd175431f19cde7a347a44d1d53f29ffecb2")
        self.assertEqual(p["postmain_ci"], {"run_id": 40072779652, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 95)
        self.assertEqual(p["event_tests"], 96)
        self.assertEqual(p["chromium_normal"], 82)
        self.assertEqual(p["chromium_strict_csp"], 82)
        self.assertEqual(p["rust_tests"], 132)
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 161)
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        q = self.data["m3_2_product_progress"]["glib_windows_target_graph_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertEqual(q["advisory"], "GHSA-wrw7-89jp-8q8g")
        self.assertEqual(q["linux_alert"], "OPEN_NOT_REMEDIATED")
        self.assertFalse(q["real_g3_authorized"])
        self.assertFalse(q["dismiss_dependabot"])
        for path in (q["tool"], q["qualification"], q["workflow"]):
            self.assertTrue((ROOT / path).is_file(), path)
        lock = (ROOT / "src-tauri/Cargo.lock").read_text(encoding="utf-8")
        self.assertEqual(lock_glib_versions(lock), ("0.18.5",))
        self.assertIn("glib", GTK_PACKAGES)
        self.assertIn("gtk", GTK_PACKAGES)
        self.assertIn("--offline", CMD)
        self.assertIn("--locked", CMD)
        self.assertIn(TRIPLE, CMD)
        self.assertEqual(CMD[0], "cargo")
        self.assertEqual(TRIPLE, "x86_64-pc-windows-msvc")
        self.assertEqual(graph_packages("glib v0.18.5\nother v1.2.3\n"),
                         {"glib": {"0.18.5"}, "other": {"1.2.3"}})
        mock = ("fabulaxiom v0.1.0\n" +
                "".join(f"crate{i} v1.0.{i}\n" for i in range(23)))
        passed = assess_windows_graph(mock)
        self.assertFalse(passed["glib_in_selected_windows_target_graph"])
        self.assertEqual(passed["historical_linux_cargo_lock_advisory"],
                         "STILL_OPEN_NOT_REMEDIATED")
        with self.assertRaisesRegex(ValueError, "STOP"):
            assess_windows_graph(mock + "glib v0.18.5\n")
        with self.assertRaisesRegex(ValueError, "STOP"):
            assess_windows_graph(mock + "gtk v0.18.2\n")
        with self.assertRaisesRegex(ValueError, "incomplete"):
            assess_windows_graph("fabulaxiom v0.1.0\n")
        workflow = (ROOT / q["workflow"]).read_text(encoding="utf-8")
        name = "      - name: M3.2 Windows Rust target GLib/GTK graph audit (no app launch)"
        self.assertEqual(workflow.count(name), 1)
        self.assertEqual(workflow.count("run: python tools/m32_glib_target_audit.py"), 1)
        self.assertTrue(workflow.index("Rust tests from lockfile") <
                        workflow.index(name) <
                        workflow.index("Rust check from lockfile"))
        for required in ("run: npm ci", "npx tsc --noEmit --pretty false",
                         "run: npm run build", "M3.2 real Chromium synthetic-only UI interaction",
                         "Verify dependency locks are unchanged"):
            self.assertIn(required, workflow)
        for name in ("RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "NEXT.md",
                     "STATE.md", "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40072779652",
                (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40072779652",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_97_pr162_terminal_and_linux_selected_gtk_glib_advisory_audit_candidate(self):
        from m32_glib_linux_target_audit import (
            CMD, FETCH_CMD, TRIPLE, ADVISORY, EXPECTED, assess_linux_graph,
        )
        p = self.data["post_pr162_terminal_observation"]
        self.assertEqual(p["pr"], 162)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "3d7c517561457add580d33151fc0bd10db3e519b")
        self.assertEqual(p["source_ci"], {"run_id": 40085001106, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "b5d97648cc18597b23f9fece67fd78b094743abb")
        self.assertEqual(p["postmain_ci"], {"run_id": 40085871815, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 96)
        self.assertEqual(p["event_tests"], 96)
        self.assertEqual(p["chromium_normal"], 82)
        self.assertEqual(p["chromium_strict_csp"], 82)
        self.assertEqual(p["rust_tests"], 132)
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 162)
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual(p["m3_2"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        q = self.data["m3_2_product_progress"]["glib_linux_selected_graph_candidate"]
        self.assertTrue(q["source_only"] and q["no_persistence"])
        self.assertFalse(q["real_g3_authorized"])
        self.assertFalse(q["dismiss_dependabot"])
        self.assertEqual(q["linux_alert"], "OPEN_NOT_REMEDIATED")
        self.assertEqual(q["advisory"], ADVISORY)
        self.assertEqual(q["windows_steps_added"], 1)
        for field in ("tool", "qualification", "workflow"):
            self.assertTrue((ROOT / q[field]).is_file(), field)
        self.assertEqual(TRIPLE, "x86_64-unknown-linux-gnu")
        self.assertIn("--offline", CMD)
        self.assertIn("--locked", CMD)
        self.assertIn(TRIPLE, CMD)
        self.assertNotIn("--all-features", CMD)
        self.assertEqual(FETCH_CMD[:2], ("cargo", "fetch"))
        self.assertIn("--locked", FETCH_CMD)
        # Cargo fetch without --target downloads the whole pinned cross-platform graph;
        # cargo tree itself is still strictly offline and Linux-selected.
        self.assertNotIn("--target", FETCH_CMD)
        self.assertNotIn(TRIPLE, FETCH_CMD)
        self.assertNotIn("--offline", FETCH_CMD)
        self.assertNotIn("--all-features", FETCH_CMD)
        self.assertEqual(EXPECTED, {
            "glib": "0.18.5", "gtk": "0.18.2", "webkit2gtk": "2.0.2",
        })
        sample = ("fabulaxiom v0.1.0\n" +
                  "".join(f"fictional{i} v1.0.{i}\n" for i in range(28)) +
                  "glib v0.18.5\ngtk v0.18.2\nwebkit2gtk v2.0.2\n")
        passed = assess_linux_graph(sample)
        self.assertEqual(passed["linux_risk_status"], "OPEN_NOT_REMEDIATED")
        self.assertEqual(passed["selected_glib"], "0.18.5")
        self.assertFalse(passed["operator_windows_access"])
        with self.assertRaisesRegex(ValueError, "STOP"):
            assess_linux_graph(sample.replace("glib v0.18.5\n", ""))
        with self.assertRaisesRegex(ValueError, "STOP"):
            assess_linux_graph(sample.replace("glib v0.18.5\n", "glib v0.20.0\n"))
        with self.assertRaisesRegex(ValueError, "STOP"):
            assess_linux_graph(sample.replace("gtk v0.18.2\n", ""))
        with self.assertRaisesRegex(ValueError, "STOP"):
            assess_linux_graph(sample.replace("webkit2gtk v2.0.2\n", ""))
        with self.assertRaisesRegex(ValueError, "incomplete"):
            assess_linux_graph("fabulaxiom v0.1.0\n")
        workflow = (ROOT / q["workflow"]).read_text(encoding="utf-8")
        name = "M3.2 Linux Rust selected GLib/GTK advisory exposure audit (no Linux build)"
        winname = "M3.2 Windows Rust target GLib/GTK graph audit (no app launch)"
        self.assertEqual(workflow.count(name), 1)
        self.assertEqual(workflow.count("run: python tools/m32_glib_linux_target_audit.py"), 1)
        self.assertTrue(workflow.index(winname) < workflow.index(name) <
                        workflow.index("Rust check from lockfile"))
        for old in ("run: npm ci", "npx tsc --noEmit --pretty false",
                    "run: npm run build", "cargo test --manifest-path",
                    "M3.2 real Chromium synthetic-only UI interaction",
                    "Verify dependency locks are unchanged"):
            self.assertIn(old, workflow)
        self.assertIn("40085871815",
            (DIRECTORY / "RESUME_PROMPT_SHORT.md").read_text(encoding="utf-8"))
        for name in ("RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            self.assertIn("40085871815",
                (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40085871815",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_98_pr163_terminal_linux_advisory_handoff(self):
        p = self.data["post_pr163_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 163)
        self.assertTrue(p["merged"])
        self.assertEqual(p["source_sha"], "46225e2843e7df2394ec2b647d4dbca20dfb6da4")
        self.assertEqual(p["source_ci"], {"run_id": 40094464488, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "7e4295160b927416d21e69e64f01fd6247d09e92")
        self.assertEqual(p["postmain_ci"], {"run_id": 40095354727, "conclusion": "SUCCESS"})
        self.assertEqual((p["source_job_steps"], p["postmain_job_steps"]), (79, 79))
        self.assertEqual((p["handoff_tests"], p["event_tests"]), (97, 96))
        self.assertEqual((p["chromium_normal"], p["chromium_strict_csp"], p["rust_tests"]), (82, 82, 132))
        self.assertEqual((p["selected_windows_graph_packages"], p["selected_linux_graph_packages"]), (247, 277))
        self.assertEqual((p["glib_linux_version"], p["gtk_linux_version"], p["webkit2gtk_linux_version"]), ("0.18.5", "0.18.2", "2.0.2"))
        self.assertEqual(p["glib_linux_alert"], "OPEN_NOT_REMEDIATED")
        self.assertFalse(p["dependabot_npm_closure_verified"])
        self.assertFalse(p["original_sqlite_touched"])
        self.assertEqual((p["m3_2"], p["g2b"], p["writer_absence"], p["g2c"], p["real_g3"]),
                         ("IN_PROGRESS_NOT_ACCEPTED", "NOT_ACCEPTED", "NOT_PROVEN", "NOT_AUTHORIZED", "STOP_UNAVAILABLE"))
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "STATE.md", "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            content = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40094464488", content, name)
            self.assertIn("40095354727", content, name)
        roadmap = (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("40095354727", roadmap)

    def test_99_pr164_terminal_and_fictional_historical_claim_intake(self):
        from m32_historical_evidence_intake import (
            ROLES, ALLOWED_FIELDS, CANDIDATE_STATUS, REJECTED_STATUS,
            MISSING_STATUS, triage_fictional_custody_claims,
        )
        p = self.data["post_pr164_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 164)
        self.assertEqual(p["source_sha"], "62868e8ac4103ecaa65d129e6e5551ff3124a99f")
        self.assertEqual(p["source_ci"], {"run_id": 40101820083, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "ac7c61f779c0981d418d8b5b7bb1d4a8a725cdbe")
        self.assertEqual(p["postmain_ci"], {"run_id": 40103615181, "conclusion": "SUCCESS"})
        self.assertEqual(p["handoff_tests"], 98)
        self.assertEqual(p["source_job_steps"], 79)
        self.assertEqual((p["event_tests"], p["chromium_normal"],
                          p["chromium_strict_csp"], p["rust_tests"]), (96, 82, 82, 132))
        self.assertFalse(p["real_g3_authorized"])
        self.assertEqual(len(ROLES), 5)
        self.assertTrue((ROOT / "docs/qualification/M3_2_HISTORICAL_EVIDENCE_INTAKE_FAIL_CLOSED_20261024.md").is_file())
        empty = triage_fictional_custody_claims([])
        self.assertEqual(set(empty["roles"]), set(ROLES))
        self.assertEqual(set(empty["roles"].values()), {MISSING_STATUS})
        safe = dict(role=ROLES[0], origin="independent_external_record",
                    proof_ref="EXT-ABCDEF12", proof_sha256="a" * 64,
                    custodian_id="ext-separate-archive",
                    preexisting_record=True, role_bound=True)
        self.assertEqual(set(safe), ALLOWED_FIELDS)
        one = triage_fictional_custody_claims([safe])
        self.assertEqual(one["roles"][ROLES[0]], CANDIDATE_STATUS)
        self.assertFalse(one["evidence_authenticated"])
        self.assertTrue(one["external_review_required"])
        variants = [
            {**safe, "origin": "owner_self_report"},
            {**safe, "proof_sha256": "not-a-digest"},
            {**safe, "custodian_id": "owner"},
            {**safe, "preexisting_record": False},
            {**safe, "role_bound": False},
            {**safe, "proof_ref": "../private/db.sqlite"},
        ]
        for claim in variants:
            with self.subTest(claim=claim):
                self.assertEqual(triage_fictional_custody_claims([claim])["roles"][ROLES[0]],
                                 REJECTED_STATUS)
        invalid = [
            [{**safe, "role": "production/unlisted"}],
            [safe, safe],
            [{**safe, "payload": "private"}],
            [safe] * 6,
            ["not-metadata"],
            "not-a-list",
        ]
        for claims in invalid:
            with self.subTest(claims=str(claims)[:24]):
                with self.assertRaises(ValueError):
                    triage_fictional_custody_claims(claims)
        all_plausible = triage_fictional_custody_claims([
            {**safe, "role": role, "proof_ref": "EXT-INVENTED" + str(index + 1).zfill(4),
             "proof_sha256": format(index + 1, "064x")}
            for index, role in enumerate(ROLES)
        ])
        self.assertEqual(set(all_plausible["roles"].values()), {CANDIDATE_STATUS})
        for report in (empty, one, all_plausible):
            self.assertEqual(report["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
            self.assertEqual(report["g2b"], "NOT_ACCEPTED")
            self.assertEqual(report["writer_absence"], "NOT_PROVEN")
            self.assertEqual(report["real_g3"], "STOP_UNAVAILABLE")
            self.assertFalse(report["operator_access"])
            self.assertFalse(report["evidence_authenticated"])
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "STATE.md", "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40103615181", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40103615181",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_100_pr165_terminal_and_no_reused_external_notice_tokens(self):
        from m32_historical_evidence_intake import (
            ROLES, CANDIDATE_STATUS, triage_fictional_custody_claims,
        )
        p = self.data["post_pr165_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 165)
        self.assertEqual(p["source_sha"], "1c592c76c48feba3ef3f5e11fca37bb0efaba03f")
        self.assertEqual(p["source_ci"], {"run_id": 40105412509, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "e1faacc909d4c8a693e2552e64dda57b6927473f")
        self.assertEqual(p["postmain_ci"], {"run_id": 40106296690, "conclusion": "SUCCESS"})
        self.assertEqual((p["source_job_steps"], p["postmain_job_steps"]), (79, 79))
        self.assertEqual((p["handoff_tests"], p["event_tests"]), (99, 96))
        self.assertEqual((p["chromium_normal"], p["chromium_strict_csp"], p["rust_tests"]),
                         (82, 82, 132))
        self.assertEqual(p["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(p["g2b"], "NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        one = dict(role=ROLES[0], origin="independent_external_record",
                   proof_ref="EXT-INVENTED0001", proof_sha256="a" * 64,
                   custodian_id="ext-archive-fictional",
                   preexisting_record=True, role_bound=True)
        reused_ref = {**one, "role": ROLES[1], "proof_sha256": "b" * 64}
        reused_sha = {**one, "role": ROLES[1], "proof_ref": "EXT-INVENTED0002"}
        for second in (reused_ref, reused_sha):
            with self.subTest(second=second):
                with self.assertRaises(ValueError):
                    triage_fictional_custody_claims([one, second])
                with self.assertRaises(ValueError):
                    triage_fictional_custody_claims([second, one])
        distinct = {**one, "role": ROLES[1],
                    "proof_ref": "EXT-INVENTED0002", "proof_sha256": "b" * 64}
        result = triage_fictional_custody_claims([one, distinct])
        self.assertEqual(set(result["roles"][role] for role in ROLES[:2]),
                         {CANDIDATE_STATUS})
        self.assertEqual(result["g2b"], "NOT_ACCEPTED")
        self.assertEqual(result["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(result["evidence_authenticated"])
        self.assertFalse(result["operator_access"])
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "STATE.md", "NEXT.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40106296690",
                          (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40106296690",
                      (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_101_pr166_terminal_and_private_recovery_sanitization(self):
        p = self.data["post_pr166_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 166)
        self.assertEqual(p["source_sha"], "fac5a230c5998eda30b6593068abca5e36d73a39")
        self.assertEqual(p["source_ci"], {"run_id": 40107790950, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "c1fee9638c343c51e2e0bdab6ac8fccf2340104b")
        self.assertEqual(p["postmain_ci"], {"run_id": 40108674282, "conclusion": "SUCCESS"})
        self.assertEqual((p["source_job_steps"], p["postmain_job_steps"]), (79, 79))
        self.assertEqual((p["handoff_tests"], p["fictional_vitest_tests"]), (100, 96))
        self.assertEqual((p["chromium_normal"], p["chromium_strict_csp"], p["rust_tests"]), (82, 82, 132))
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(p["g2b"], "NOT_ACCEPTED")
        self.assertEqual(p["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertFalse(p["original_sqlite_access"])
        doc = (ROOT / "docs/qualification/M3_2_RECOVERED_COPIES_RECONCILIATION_20261024.md").read_text(encoding="utf-8")
        for role in ("pre_m24_early_manifest", "original_acls", "pre_repair_json",
                     "activation_marker", "isolated_v6"):
            self.assertIn(role, doc)
        for required in ("0/5", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                         "DONNEES_PRIVEES_NON_PUBLIEES", "STOP_UNAVAILABLE"):
            self.assertIn(required, doc)
        # Only the three historically published observed hashes are recognized;
        # the current private SQLite candidate and original files are excluded.
        self.assertNotIn("C:\\Users\\", doc)
        self.assertNotIn("S-1-5-21-", doc)
        self.assertNotIn("M:\\", doc)
        self.assertNotIn("SQLite format 3", doc)  # no binary artifact bytes
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "STATE.md", "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40108674282", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40108674282",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_102_pr167_terminal_detached_ram_only_and_solo_g2_plan(self):
        p = self.data["post_pr167_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 167)
        self.assertEqual(p["source_sha"], "819dbb0a1d80a07e9c19b3e7eacff761dce8dc9b")
        self.assertEqual(p["source_ci"], {"run_id": 40115530223, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "533bdb27480a2b6dbed630b148501eeaf3c34b1e")
        self.assertEqual(p["postmain_ci"], {"run_id": 40116658246, "conclusion": "SUCCESS"})
        self.assertEqual((p["source_job_steps"], p["postmain_job_steps"]), (79, 79))
        self.assertEqual((p["handoff_tests"], p["fictional_vitest_tests"]), (101, 96))
        self.assertEqual((p["chromium_normal"], p["chromium_strict_csp"], p["rust_tests"]), (82, 82, 132))
        self.assertEqual(p["g2b"], "NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(p["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertFalse(p["operator_windows_access"])
        q = self.data["detached_m25_ram_validation_observation"]
        self.assertTrue(q["sqlite_ram_deserialize_only"])
        self.assertEqual(q["integrity_check"], "ok")
        self.assertEqual(q["foreign_key_violations"], 0)
        self.assertEqual(q["schema_migrations"], [1, 2, 3, 4, 5, 6])
        self.assertEqual(q["application_tables"], 14)
        self.assertFalse(q["private_candidate_digest_in_github"])
        self.assertFalse(q["historical_m25_identity_proven"])
        self.assertFalse(q["operator_files_opened"])
        self.assertEqual(q["historical_attestations_verified"], 0)
        doc = (ROOT / "docs/qualification/M3_2_RECOVERED_COPIES_RECONCILIATION_20261024.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/qualification/M3_2_G2_RECOVERED_COPIES_SOLO_APPROVAL_SCOPE_20261024.md").read_text(encoding="utf-8")
        for content in (doc, plan):
            for required in ("integrity_check", "foreign_key_check", "M2.5",
                             "NOT_ACCEPTED", "STOP_UNAVAILABLE"):
                self.assertIn(required, content)
            for forbidden in ("C:\\Users\\", "S-1-5-21-", "M:\\"):
                self.assertNotIn(forbidden, content)
            import re
            self.assertIsNone(re.search(r"(?<![A-Za-z0-9])[a-f0-9]{64}(?![A-Za-z0-9])", content))
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "STATE.md", "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40116658246", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        self.assertIn("40116658246",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))

    def test_103_pr168_terminal_g2b0_unexecuted_text_only(self):
        p = self.data["post_pr168_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 168)
        self.assertEqual(p["source_sha"], "d1f6db636a09112ace772b734c1a33e81d63d168")
        self.assertEqual(p["source_ci"], {"run_id": 40117705107, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "a03cc5dad68aaf4cb78c39520de130960dc565f8")
        self.assertEqual(p["postmain_ci"], {"run_id": 40122346098, "conclusion": "SUCCESS"})
        self.assertEqual((p["source_steps"], p["postmain_steps"]), (79, 79))
        self.assertEqual((p["handoff_tests"], p["vitest_tests"],
                          p["chromium_normal"], p["chromium_strict_csp"],
                          p["rust_tests"]), (102, 96, 82, 82, 132))
        self.assertFalse(p["operator_windows_access"])
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        path = ROOT / "docs/qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md"
        document = path.read_text(encoding="utf-8")
        import re
        blocks = re.findall(r"(?ms)^`{3}powershell\s*\n(.*?)^`{3}\s*$", document)
        self.assertEqual(len(blocks), 1)
        script = blocks[0]
        self.assertTrue(script.startswith("& {\n"))
        self.assertTrue(script.rstrip().endswith("}"))
        for required in (
            "Get-Process -ErrorAction Stop", "Get-Item -LiteralPath",
            "Get-ChildItem -LiteralPath", "REPARSE_ANCESTOR",
            "SQLITE_SIDECAR_SEEN", "OBSERVED_PARTIAL_ONLY",
            "M31_V7_AND_OTHER_ROLES: NOT_ASSESSED",
            "G2B_SOURCE_IDENTITY: PARTIAL_LOCAL_IDENTITY_ONLY",
            "SQLITE_WRITER_ABSENCE: NOT_PROVEN",
            "G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED",
        ):
            self.assertIn(required, script)
        for unsafe in ("Get-FileHash", "Get-Acl", "Get-Content",
                       "Stop-Process", "Start-Process", "Add-Type",
                       "Invoke-Expression", "Invoke-WebRequest",
                       "Remove-Item", "Copy-Item", "Set-Content",
                       "Set-Acl", "Start-Transcript", "sqlite3.exe",
                       "Get-ItemProperty"):
            self.assertNotIn(unsafe, script)
        self.assertNotIn("C:\\Users\\", document)
        self.assertNotIn("S-1-5-21-", document)
        self.assertIn("PREPARED_NOT_EXECUTED", document)
        self.assertIn("STOP_UNAVAILABLE", document)
        for f in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                  "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                  "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40122346098", (DIRECTORY / f).read_text(encoding="utf-8"))
        self.assertIn("40122346098",
            (ROOT / "docs/roadmap/ROADMAP_STATUS_CURRENT.md").read_text(encoding="utf-8"))


    def test_104_pr169_terminal_and_g2b0_ast_static_only(self):
        p = self.data["post_pr169_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 169)
        self.assertEqual(p["source_sha"], "67e2b400510fe4bade797a9fd73997f892ded1ad")
        self.assertEqual(p["source_ci"], {"run_id": 40127450956, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "4ea2c5f9ad380863c5634dae65faac9831b1cec3")
        self.assertEqual(p["postmain_ci"], {"run_id": 40128407418, "conclusion": "SUCCESS"})
        self.assertEqual(p["postmain_job_steps"], 79)
        self.assertFalse(p["g2b0_executed"])
        self.assertFalse(p["operator_approved"])
        self.assertFalse(p["operator_windows_access"])
        self.assertEqual(p["m32"], "IN_PROGRESS_NOT_ACCEPTED")
        self.assertEqual(p["g2b"], "NOT_ACCEPTED")
        self.assertEqual(p["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(p["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        guard = (ROOT / "tools/m32_g2b0_ast_static_review.ps1").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/m0-ci.yml").read_text(encoding="utf-8")
        for required in ("Parser]::ParseInput", "Test-G2B0SourceAstShape",
                         "InvokeMemberExpressionAst", "RedirectionAst",
                         "STOP_G2B0", "M32_G2B0_AST_STATIC_REVIEW_PASS",
                         "M32_G2B0_OPERATOR_AUTHORIZATION: NOT_GRANTED",
                         "M32_G2B0_WINDOWS_OS_SAFETY: NOT_CERTIFIED",
                         "Remove-Item", "WriteAllText"):
            self.assertIn(required, guard)
        self.assertIn("run: ./tools/m32_g2b0_ast_static_review.ps1", workflow)
        self.assertIn("no candidate execution", workflow)
        self.assertNotIn("Invoke-Expression $candidate", guard)
        proposal = (ROOT / "docs/qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_NOT_EXECUTED", proposal)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40128407418", doc, name)
        for path in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40128407418", (ROOT / "docs/roadmap" / path).read_text(encoding="utf-8"))


    def test_105_pr170_postmain_b0_owner_report_and_b1_candidate(self):
        record = self.data["post_pr170_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 170)
        self.assertEqual(record["source_sha"], "458f58ad6960b72b81fbfbe588f90168e36c3975")
        self.assertEqual(record["source_ci"], {"run_id": 40155313316, "conclusion": "SUCCESS"})
        self.assertEqual(record["merge_sha"], "93eba0ae4801e5a0a73121fef305dc9212e52761")
        self.assertEqual(record["postmain_ci"], {"run_id": 40156277835, "conclusion": "SUCCESS"})
        self.assertEqual((record["source_steps"], record["postmain_steps"], record["handoff_tests"]),
                         (80, 80, 104))
        self.assertEqual((record["fictional_vitest_tests"], record["chromium_normal"],
                          record["chromium_strict_csp"], record["rust_tests"]),
                         (96, 82, 82, 132))
        self.assertFalse(record["operator_windows_access"])
        self.assertEqual(record["real_g3"], "STOP_UNAVAILABLE")
        owner = self.data["g2b0_operator_report_20261025"]
        self.assertEqual(owner["observation"], "OBSERVED_PARTIAL_ONLY_OWNER_REPORTED")
        self.assertEqual((owner["production_m15_sqlite_filename_count"],
                          owner["isolated_m25_sqlite_filename_count"]), (4, 1))
        self.assertTrue(owner["operator_local_run_reported"])
        self.assertFalse(owner["independent_attestation"])
        self.assertEqual(owner["writer_absence"], "NOT_PROVEN")
        self.assertEqual(owner["g2c"], "NOT_AUTHORIZED")
        b1 = self.data["g2b1_selector_review"]
        self.assertEqual(b1["status"], "OBSERVED_PARTIAL_ONLY_OWNER_REPORTED")
        self.assertEqual(b1["g2b"], "NOT_ACCEPTED")
        self.assertTrue(b1["no_original_sqlite_read"])
        doc = (ROOT / "docs/qualification/M3_2_G2B1_ACTIVATION_SELECTOR_REVIEW_20261025.md").read_text(encoding="utf-8")
        guard = (ROOT / "tools/m32_g2b1_ast_static_review.ps1").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/m0-ci.yml").read_text(encoding="utf-8")
        import re
        blocks = re.findall(r"(?ms)^`{3}powershell\s*\n(.*?)^`{3}\s*$", doc)
        self.assertEqual(len(blocks), 1)
        script = blocks[0]
        for snippet in ("[IO.File]::ReadAllText", "MARKER_SIZE",
                        "if ($sqlite.Count -ne 4)", "SQLITE_WRITER_ABSENCE: NOT_PROVEN",
                        "G2B1_SELECTOR_OBSERVATION: OBSERVED_PARTIAL_ONLY",
                        "G2C_G2D_G3_G4_G5_G6: NOT_AUTHORIZED"):
            self.assertIn(snippet, script)
        for snippet in ("Get-FileHash", "Get-Acl", "Stop-Process", "Set-Content",
                        "Copy-Item", "Remove-Item", "sqlite3.exe", "Invoke-Expression"):
            self.assertNotIn(snippet, script)
        self.assertIn("Parser]::ParseInput", guard)
        self.assertIn("fakeChanges", guard)
        self.assertIn("run: ./tools/m32_g2b1_ast_static_review.ps1", workflow)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40156277835", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40156277835", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)


    def test_106_pr171_terminal_b1_owner_result_and_custody_route_stop(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 171)
        p = self.data["post_pr171_terminal_observation"]
        self.assertEqual(p["source_sha"], "6912ba98ebbd558ac86a5669a497f757df990db2")
        self.assertEqual(p["source_ci"], {"run_id": 40166867332, "conclusion": "SUCCESS"})
        self.assertEqual(p["merge_sha"], "a33600120f78f20477f4680737e87cb9fabf818b")
        self.assertEqual(p["postmain_ci"], {"run_id": 40169967245, "conclusion": "SUCCESS"})
        self.assertEqual((p["source_steps"], p["postmain_steps"], p["handoff_tests"]),
                         (81, 81, 105))
        self.assertEqual((p["fictional_vitest_tests"], p["chromium_normal"],
                          p["chromium_strict_csp"], p["rust_tests"]), (96, 82, 82, 132))
        self.assertFalse(p["operator_windows_access"])
        owner = self.data["g2b1_operator_report_20261025"]
        self.assertTrue(owner["operator_local_run_reported"])
        self.assertFalse(owner["independently_attested"])
        self.assertEqual(owner["status"], "OBSERVED_PARTIAL_ONLY_OWNER_REPORTED")
        self.assertEqual(owner["production_m15_sqlite_filename_count"], 4)
        self.assertEqual(owner["accepted_activation_marker_count"], 1)
        self.assertEqual(owner["selector_kind"], "RESTORED")
        self.assertEqual(owner["selected_filename_match"], "ONE_OBSERVED")
        self.assertEqual(owner["source_identity"], "PARTIAL_LOCAL_IDENTITY_ONLY")
        self.assertEqual(owner["writer_absence"], "NOT_PROVEN")
        self.assertEqual(owner["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(owner["g3"], "STOP_UNAVAILABLE")
        self.assertEqual(owner["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(owner["prospective"], "NOT_STARTED")
        decision = self.data["next_source_custody_route_decision_20261025"]
        self.assertEqual(decision["route_a_preopened_owner"], "UNAVAILABLE_NOT_PROVEN")
        self.assertEqual(decision["route_b_cold_quiescence"], "NOT_PROVEN")
        self.assertEqual(decision["route_c_greenfield"], "DEVELOPMENT_ONLY")
        self.assertEqual(decision["g2b"], "NOT_ACCEPTED")
        self.assertEqual(decision["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(decision["windows_operator_new_procedure"], "NOT_PROPOSED")
        path = ROOT / decision["document"]
        document = path.read_text(encoding="utf-8")
        for required in ("PR #171", "40169967245", "OBSERVED_PARTIAL_ONLY",
                         "UNAVAILABLE_NOT_PROVEN", "DEVELOPMENT_ONLY",
                         "NOT_ACCEPTED", "NOT_PROVEN", "STOP_UNAVAILABLE",
                         "PENDING_EXTERNAL_ATTESTATION(21/3/2)", "NOT_STARTED",
                         "No automatic escalation"):
            self.assertIn(required, document)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40169967245", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40169967245", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)


    def test_107_pr172_terminal_and_invented_shared_ram_writer_counterexample(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 172)
        q = self.data["post_pr172_terminal_observation"]
        self.assertEqual(q["source_sha"], "dd652e7be13e73b3612e663284afc4da5d785f4f")
        self.assertEqual(q["source_ci"], {"run_id": 40178558404, "conclusion": "SUCCESS"})
        self.assertEqual(q["merge_sha"], "51e4264b463f60bd8186d09a8ac306315b39d79d")
        self.assertEqual(q["postmain_ci"], {"run_id": 40179336243, "conclusion": "SUCCESS"})
        self.assertEqual((q["source_steps"], q["postmain_steps"], q["handoff_tests"]),
                         (81, 81, 106))
        self.assertEqual((q["fictional_vitest_tests"], q["chromium_normal"],
                          q["chromium_strict_csp"], q["rust_tests"]), (96, 82, 82, 132))
        self.assertFalse(q["operator_windows_access"])
        self.assertEqual(q["g2b"], "NOT_ACCEPTED")
        self.assertEqual(q["writer"], "NOT_PROVEN")
        self.assertEqual(q["real_g3"], "STOP_UNAVAILABLE")
        negative = self.data["next_invented_shared_ram_writer_negative_20261025"]
        self.assertEqual(negative["scope"], "SYNTHETIC_TEST_ONLY")
        self.assertEqual(negative["new_rust_test_count"], 2)
        self.assertEqual(negative["writer_absence"], "NOT_PROVEN")
        self.assertEqual(negative["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(negative["actual_windows_operator_access"])
        source = (ROOT / "src-tauri/src/m32_preopened_query_only_toy.rs").read_text(encoding="utf-8")
        report = (ROOT / negative["document"]).read_text(encoding="utf-8")
        for name in negative["test_names"]:
            self.assertIn("fn " + name, source)
        for required in ("mode=memory&cache=shared", "PRAGMA query_only=ON",
                         "total_changes(&reader)?", "other_writer.execute",
                         "fictitious external rewrite", "lease.read_again()"):
            self.assertIn(required, source)
        for forbidden in ("database::open_database(", "restore_backup(",
                          "std::fs::", "OpenOptions", "std::process::Command"):
            self.assertNotIn(forbidden, source)
        for required in ("SYNTHETIC_COUNTEREXAMPLE_ONLY", "NOT_PROVEN",
                         "STOP_UNAVAILABLE", "40179336243",
                         "PRAGMA query_only", "total_changes()"):
            self.assertIn(required, report)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40179336243", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40179336243", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"))


    def test_108_post_pr173_terminal_and_data_version_invented_ram_guard(self):
        self.assertEqual(self.data["last_confirmed_merged_pr"], 173)
        last = self.data["post_pr173_terminal_observation"]
        self.assertEqual(last["source_sha"], "a44e9b946f1f420c44f1403f412fb59ccca9a284")
        self.assertEqual(last["source_ci"], {"run_id": 40189597795, "conclusion": "SUCCESS"})
        self.assertEqual(last["merge_sha"], "63faae23c63ae0012f74c63aad730d93f95ce1c2")
        self.assertEqual(last["postmain_ci"], {"run_id": 40190429389, "conclusion": "SUCCESS"})
        self.assertEqual((last["steps_source"], last["steps_postmain"], last["handoff_tests"]),
                         (81, 81, 107))
        self.assertEqual((last["fictional_vitest_tests"], last["chromium_normal"],
                          last["chromium_strict_csp"], last["rust_tests"]), (96, 82, 82, 132))
        self.assertFalse(last["operator_windows_access"])
        self.assertEqual(last["real_g3"], "STOP_UNAVAILABLE")
        planned = self.data["next_data_version_synthetic_cross_connection_guard_20261025"]
        self.assertEqual(planned["status"], "CANDIDATE_SYNTHETIC_TEST_ONLY")
        self.assertEqual(planned["new_rust_test_count"], 4)
        self.assertEqual(planned["comparison"], "SAME_CONNECTION_ONLY")
        self.assertEqual(planned["global_writer_absence"], "NOT_PROVEN")
        self.assertEqual(planned["source_provenance"], "NOT_PROVEN")
        self.assertEqual(planned["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(planned["operator_windows_actions"])
        rust = (ROOT / "src-tauri/src/m32_preopened_query_only_toy.rs").read_text(encoding="utf-8")
        doc = (ROOT / planned["document"]).read_text(encoding="utf-8")
        for name in planned["test_names"]:
            self.assertIn("fn " + name, rust)
        for snippet in ("struct VersionedFictionalReader", "PRAGMA data_version",
                        "local_data_version(self.old_guard.source)?",
                        "PreopenedFictionalReader::new", "mode=memory&cache=shared",
                        "fn toy_14_query_only_and_total_changes_do_not_exclude_independent_writer"):
            self.assertIn(snippet, rust)
        for forbidden in ("Connection::open(operator_path)", "database::open_database(",
                          "std::fs::", "#[tauri::command]", "VACUUM INTO"):
            self.assertNotIn(forbidden, rust)
        for snippet in ("SYNTHÉTIQUES UNIQUEMENT", "NOT_PROVEN",
                        "STOP_UNAVAILABLE", "40190429389", "PRAGMA data_version"):
            self.assertIn(snippet, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            self.assertIn("40190429389", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40190429389", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)

if __name__ == "__main__":
    unittest.main()
