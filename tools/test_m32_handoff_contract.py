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
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 173)
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


    def test_109_pr174_postmain_and_ram_transaction_custody_boundary(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 174)
        state = self.data["post_pr174_terminal_observation"]
        self.assertEqual(state["source_sha"], "a9a031e3f7322e39475c70c2a1111fdc0c37f047")
        self.assertEqual(state["source_ci"], {"run_id": 40199121197, "conclusion": "SUCCESS"})
        self.assertEqual(state["merge_sha"], "0c1aee574832a3f48571546b345ebaad9228c163")
        self.assertEqual(state["postmain_ci"], {"run_id": 40200127549, "conclusion": "SUCCESS"})
        self.assertEqual((state["source_steps"], state["postmain_steps"], state["handoff_tests"]), (81, 81, 108))
        self.assertEqual((state["fictional_vitest_tests"], state["chromium_normal"],
                          state["chromium_strict_csp"], state["rust_tests"]), (96, 82, 82, 132))
        self.assertFalse(state["operator_windows_access"])
        self.assertEqual(state["real_g3"], "STOP_UNAVAILABLE")
        case = self.data["next_ram_transaction_custody_window_negative_20261025"]
        self.assertEqual(case["scope"], "SYNTHETIC_TEST_ONLY")
        self.assertEqual(case["new_rust_tests"], 2)
        self.assertFalse(case["postflight_is_lock"])
        self.assertEqual(case["transaction_mode"], "INVENTED_RAM_SHARED_CACHE_ONLY")
        self.assertEqual(case["generalized_writer_absence"], "NOT_PROVEN")
        self.assertEqual(case["g2b"], "NOT_ACCEPTED")
        self.assertEqual(case["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(case["operator_windows_actions"])
        rust = (ROOT / "src-tauri/src/m32_preopened_query_only_toy.rs").read_text(encoding="utf-8")
        doc = (ROOT / case["document"]).read_text(encoding="utf-8")
        for name in case["test_names"]:
            self.assertIn("fn " + name + "(", rust)
        for expected in ("mode=memory&cache=shared", "BEGIN DEFERRED TRANSACTION",
                         "invented concurrent write", "invented after-release write",
                         "invented postflight write", "reader.execute_batch(\"ROLLBACK;\")?",
                         "local_data_version(&reader)?", "rusqlite::ErrorCode::DatabaseLocked"):
            self.assertIn(expected, rust)
        for forbidden in ("database::open_database(", "std::fs::", "OpenOptions",
                          "std::process::Command", "VACUUM INTO", "#[tauri::command]"):
            self.assertNotIn(forbidden, rust)
        for expected in ("40199121197", "40200127549",
                         "SYNTHETIC", "NOT_PROVEN", "STOP_UNAVAILABLE",
                         "toy_20", "toy_21"):
            self.assertIn(expected, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40200127549", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40200127549", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)



    def test_110_pr175_terminal_and_shared_ram_table_scope_isolation_candidates(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 175)
        terminal = self.data["post_pr175_terminal_observation"]
        self.assertEqual(terminal["source_sha"], "bd5e8ef35b80d653530f1f36d288724c1642f2ea")
        self.assertEqual(terminal["source_ci"], {"run_id": 40209991293, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "c7d93dd2844bdd3cb17c5ffb5cc600902f9ba18f")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40210737724, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["source_steps"], terminal["postmain_passed_steps"],
                          terminal["postmain_skipped_steps"], terminal["handoff_tests"]),
                         (81, 80, 1, 109))
        self.assertEqual((terminal["fictional_vitest_tests"], terminal["chromium_normal"],
                          terminal["chromium_strict_csp"], terminal["rust_tests"]),
                         (96, 82, 82, 132))
        self.assertFalse(terminal["operator_windows_access"])
        self.assertEqual(terminal["real_g3"], "STOP_UNAVAILABLE")
        case = self.data["next_shared_ram_table_scope_and_isolation_negative_20261025"]
        self.assertEqual(case["scope"], "SYNTHETIC_TEST_ONLY")
        self.assertEqual(case["new_rust_tests"], 2)
        self.assertFalse(case["database_wide_writer_exclusion"])
        self.assertEqual(case["isolation"], "SHARED_CACHE_READ_UNCOMMITTED_ONLY")
        self.assertEqual(case["global_writer_absence"], "NOT_PROVEN")
        self.assertEqual(case["g2b"], "NOT_ACCEPTED")
        self.assertEqual(case["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(case["operator_windows_actions"])
        rust = (ROOT / "src-tauri/src/m32_preopened_query_only_toy.rs").read_text(encoding="utf-8")
        doc = (ROOT / case["document"]).read_text(encoding="utf-8")
        for name in case["test_names"]:
            self.assertIn("fn " + name + "(", rust)
        for expected in ("imaginary_other_events", "invented other-table write",
                         "invented locked-table write", "rusqlite::ErrorCode::DatabaseLocked",
                         "PRAGMA read_uncommitted=ON", "invented uncommitted-mode write",
                         "reader.execute_batch(\"ROLLBACK;\")?"):
            self.assertIn(expected, rust)
        for forbidden in ("database::open_database(", "std::fs::", "OpenOptions",
                          "std::process::Command", "VACUUM INTO", "#[tauri::command]"):
            self.assertNotIn(forbidden, rust)
        for expected in ("40209991293", "40210737724", "SYNTHETIC_TEST_ONLY",
                         "NOT_PROVEN", "STOP_UNAVAILABLE", "toy_22", "toy_23"):
            self.assertIn(expected, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40210737724", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40210737724", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)

    def test_111_pr176_terminal_and_shared_ram_dirty_read_rollback_candidates(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 176)
        state = self.data["post_pr176_terminal_observation"]
        self.assertEqual(state["source_sha"], "8b889049c118d7a8dcea21b5ce77a6bd2ce2b278")
        self.assertEqual(state["source_ci"], {"run_id": 40212798456, "conclusion": "SUCCESS"})
        self.assertEqual(state["merge_sha"], "254384336d8c086fefec769c41cb7723112c9077")
        self.assertEqual(state["postmain_ci"], {"run_id": 40213790809, "conclusion": "SUCCESS"})
        self.assertEqual((state["source_steps"], state["postmain_passed_steps"],
                          state["postmain_skipped_steps"], state["handoff_tests"]), (81, 80, 1, 110))
        self.assertEqual((state["fictional_vitest_tests"], state["chromium_normal"],
                          state["chromium_strict_csp"], state["rust_tests"]), (96, 82, 82, 132))
        self.assertFalse(state["operator_windows_access"])
        self.assertEqual(state["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(state["earlier_failed_source_ci"]["run_id"], 40212633142)
        case = self.data["next_shared_ram_dirty_read_rollback_20261025"]
        self.assertEqual(case["scope"], "SYNTHETIC_TEST_ONLY")
        self.assertEqual(case["new_rust_tests"], 2)
        self.assertFalse(case["dirty_read_is_committed"])
        self.assertFalse(case["data_version_detects_rollback"])
        self.assertEqual(case["global_writer_absence"], "NOT_PROVEN")
        self.assertEqual(case["g2b"], "NOT_ACCEPTED")
        self.assertEqual(case["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(case["operator_windows_actions"])
        rust = (ROOT / "src-tauri/src/m32_preopened_query_only_toy.rs").read_text(encoding="utf-8")
        doc = (ROOT / case["document"]).read_text(encoding="utf-8")
        for name in case["test_names"]:
            self.assertIn("fn " + name + "(", rust)
        for expected in ("mode=memory&cache=shared", "PRAGMA read_uncommitted=ON",
                         "invented dirty transient value", "invented rolled-back row",
                         "writer.execute_batch(\"ROLLBACK;\")?",
                         "assert_eq!(local_data_version(&reader)?, initial_version)"):
            self.assertIn(expected, rust)
        for forbidden in ("database::open_database(", "std::fs::", "OpenOptions",
                          "std::process::Command", "VACUUM INTO", "#[tauri::command]"):
            self.assertNotIn(forbidden, rust)
        for expected in ("40212798456", "40213790809", "SYNTHETIC_TEST_ONLY",
                         "NOT_PROVEN", "STOP_UNAVAILABLE", "toy_24", "toy_25"):
            self.assertIn(expected, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40213790809", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40213790809", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)

    def test_112_pr177_terminal_and_repeated_dirty_read_negative_candidate(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 177)
        terminal = self.data["post_pr177_terminal_observation"]
        self.assertEqual(terminal["source_sha"], "32093f7f31f26c98e7b91bc9d25930ee4f973d27")
        self.assertEqual(terminal["source_ci"], {"run_id": 40219228723, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "c1868256739247810ecf6b606e051b53b8c0d529")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40220215000, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["source_steps"], terminal["postmain_passed_steps"],
                          terminal["postmain_skipped_steps"], terminal["handoff_tests"]),
                         (81, 80, 1, 111))
        self.assertEqual((terminal["fictional_vitest_tests"], terminal["chromium_normal"],
                          terminal["chromium_strict_csp"], terminal["rust_tests"]),
                         (96, 82, 82, 132))
        self.assertFalse(terminal["operator_windows_access"])
        self.assertEqual(terminal["real_g3"], "STOP_UNAVAILABLE")
        case = self.data["next_shared_ram_double_sample_dirty_read_20261025"]
        self.assertEqual(case["scope"], "SYNTHETIC_TEST_ONLY")
        self.assertEqual(case["new_rust_tests"], 1)
        self.assertFalse(case["two_equal_samples_prove_committed"])
        self.assertFalse(case["local_total_changes_detects_peer_writer"])
        self.assertFalse(case["data_version_detects_rollback"])
        self.assertFalse(case["query_only_prevents_dirty_read"])
        self.assertEqual(case["global_writer_absence"], "NOT_PROVEN")
        self.assertEqual(case["g2b"], "NOT_ACCEPTED")
        self.assertEqual(case["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(case["operator_windows_actions"])
        rust = (ROOT / "src-tauri/src/m32_preopened_query_only_toy.rs").read_text(encoding="utf-8")
        doc = (ROOT / case["document"]).read_text(encoding="utf-8")
        self.assertIn("fn " + case["test_name"] + "(", rust)
        for expected in ("mode=memory&cache=shared", "PRAGMA read_uncommitted=ON",
                         "PRAGMA query_only", "invented twice-observed dirty value",
                         "for _sample in 0..2", "total_changes(&reader)?",
                         "local_data_version(&reader)?",
                         'writer.execute_batch("ROLLBACK;")?'):
            self.assertIn(expected, rust)
        for forbidden in ("database::open_database(", "std::fs::", "OpenOptions",
                          "std::process::Command", "VACUUM INTO", "#[tauri::command]"):
            self.assertNotIn(forbidden, rust)
        for expected in ("40219228723", "40220215000", "SYNTHETIC_TEST_ONLY",
                         "NOT_PROVEN", "STOP_UNAVAILABLE", "toy_26"):
            self.assertIn(expected, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40220215000", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40220215000", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)

    def test_113_pr178_terminal_and_source_only_evidence_ceiling(self):
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 178)
        terminal = self.data["post_pr178_terminal_observation"]
        self.assertEqual(terminal["source_sha"], "c13a166f07c4850258628db5279594699b5ccfe8")
        self.assertEqual(terminal["source_ci"], {"run_id": 40229362824, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "dd5e6f17c6a4d71f4ac19ba0da4821a362f2af7d")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40230066592, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["source_steps"], terminal["postmain_passed_steps"],
                          terminal["postmain_skipped_steps"], terminal["handoff_tests"]),
                         (81, 80, 1, 112))
        self.assertEqual((terminal["fictional_vitest_tests"], terminal["chromium_normal"],
                          terminal["chromium_strict_csp"], terminal["rust_tests"]),
                         (96, 82, 82, 132))
        self.assertFalse(terminal["operator_windows_access"])
        self.assertEqual(terminal["real_g3"], "STOP_UNAVAILABLE")
        ceiling = self.data["next_g2b_g3_source_only_evidence_ceiling_20261025"]
        self.assertEqual(ceiling["scope"], "SOURCE_ONLY_CLASSIFICATION_NOT_OPERATOR_ATTESTATION")
        self.assertEqual(ceiling["new_rust_tests"], 0)
        for key in ("new_operator_evidence", "owner_report_is_independent_attestation",
                    "synthetic_ci_proves_real_quiescence", "source_audit_is_live_custody",
                    "operator_windows_actions"):
            self.assertFalse(ceiling[key], key)
        self.assertEqual((ceiling["route_a"], ceiling["route_b"], ceiling["route_c"]),
                         ("UNAVAILABLE_NOT_PROVEN", "NOT_PROVEN", "DEVELOPMENT_ONLY"))
        self.assertEqual(ceiling["global_writer_absence"], "NOT_PROVEN")
        self.assertEqual(ceiling["g2b"], "NOT_ACCEPTED")
        self.assertEqual(ceiling["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(ceiling["real_g3"], "STOP_UNAVAILABLE")
        self.assertEqual(ceiling["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(ceiling["prospective"], "NOT_STARTED")
        self.assertEqual(self.data["governance"]["historic"], ceiling["historical"])
        self.assertEqual(self.data["governance"]["prospective"], ceiling["prospective"])
        doc = (ROOT / ceiling["document"]).read_text(encoding="utf-8")
        for expected in ("40229362824", "40230066592", "NO_ELIGIBLE_REAL_G3_STRATEGY_STOP",
                         "OWNER_REPORTED", "SOURCE-ONLY", "UNAVAILABLE_NOT_PROVEN",
                         "DEVELOPMENT_ONLY", "NOT_PROVEN", "STOP_UNAVAILABLE",
                         "PENDING_EXTERNAL_ATTESTATION(21/3/2)", "PR #35",
                         "M3_2_G3_TAURI_OWNER_INTEGRATION_AUDIT.md",
                         "M3_2_POST_G2B1_CUSTODY_ROUTE_DECISION_20261025.md",
                         "FILE_SHARE_WRITE", "read_uncommitted"):
            self.assertIn(expected, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                     "HANDOFF_CURRENT.md", "HANDOFF_HISTORY.md", "STATE.md",
                     "NEXT.md", "M3_2_GATE_DECISION_CURRENT.md", "README.md",
                     "HANDOFF_PROTOCOL.md"):
            self.assertIn("40230066592", (DIRECTORY / name).read_text(encoding="utf-8"), name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40230066592", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"), name)

    def test_114_pr183_operator_archive_five_of_five_and_windows_path_handoff(self):
        """An owner report is useful product feedback, never historic attestation."""
        observation = self.data["post_pr183_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 183)
        self.assertEqual(observation["merge_sha"],
                         "39725a020a8656b8d0488628bc208fcf104c058c")
        self.assertEqual(observation["source_ci"], {"run_id": 40309445029, "conclusion": "SUCCESS"})
        self.assertEqual(observation["postmain_ci"], {"run_id": 40310982760, "conclusion": "SUCCESS"})
        self.assertEqual(observation["operator_archive_result"],
                         "OWNER_REPORTED_GREENFIELD_REVISION_ARCHIVE_5_OF_5_PASS")
        self.assertEqual(observation["issue38_operator_archive_five_of_five_comment"], 6417653782)
        for key in ("independent_operator_attestation", "release_qualified", "m3_2_accepted",
                    "original_sqlite_access", "migration_007_invoked"):
            self.assertFalse(observation[key], key)
        locations = self.data["operator_windows_route_c_paths_20261026"]
        self.assertEqual(locations["source_clone_owner_reported"], r"M:\Fabulaxiom")
        self.assertEqual(locations["profile"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(locations["greenfield_database_owner_reported"],
                         r"%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3")
        self.assertTrue(locations["greenfield_database_is_outside_git"])
        self.assertEqual(locations["historical_sqlite_locations"],
                         "INTENTIONALLY_NOT_PUBLISHED_OR_PROBED")
        self.assertEqual(locations["windows_powershell_command_encapsulation"], "& { ... }")
        self.assertFalse(locations["backup_restore_on_existing_operator_profile_authorized"])
        self.assertFalse(locations["historical_storage_access_authorized"])
        self.assertFalse(locations["operator_report_is_independent_attestation"])
        memo = ROOT / locations["document"]
        self.assertTrue(memo.is_file())
        doc = memo.read_text(encoding="utf-8")
        for required in (r"M:\Fabulaxiom", r"M:\Fabulaxiom\src-tauri",
                         "RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md",
                         "OWNER_REPORTED_GREENFIELD_REVISION_ARCHIVE_5_OF_5_PASS",
                         "6417653782", "IN_PROGRESS_NOT_ACCEPTED"):
            self.assertIn(required, doc)
        self.assertNotIn("C:\\Users\\", doc)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            s = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md", s, filename)
            self.assertIn("40310982760", s, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            s = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md", s, filename)
            self.assertIn("40310982760", s, filename)
        self.assertIn("M:\\Fabulaxiom", (DIRECTORY / "RESUME_PROMPT_SHORT.md").read_text(encoding="utf-8"))
        self.assertEqual(self.data["governance"]["historic"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(self.data["governance"]["prospective"], "NOT_STARTED")

    def test_115_pr184_terminal_and_unqualified_new_only_backup_restore(self):
        terminal = self.data["post_pr184_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 184)
        self.assertEqual(terminal["merge_sha"], "810a31b22dabb0507d43d83dd1b5b374916bf13b")
        self.assertEqual(terminal["source_ci"], {"run_id": 40336276164, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40338104050, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["handoff_tests"], 114)
        self.assertEqual(terminal["issue38_terminal_comment"], 6418543539)
        self.assertFalse(terminal["operator_restore_performed"])
        self.assertFalse(terminal["m3_2_accepted"])
        candidate = self.data["next_route_c_new_only_backup_restore_fixtures_20261026"]
        self.assertEqual(candidate["scope"], "RUNNER_ONLY")
        self.assertEqual(candidate["decision"], "EXISTING_PROFILE_RESTORE_BLOCKED")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual((candidate["greenfield_ci_cases_expected"],
                          candidate["source_guard_cases_expected"]), (3, 5))
        self.assertTrue(candidate["preserves_archived_revision_text_and_metadata"])
        self.assertTrue(candidate["demonstrates_occupied_root_changes_active_selection"])
        for key in ("has_production_fresh_destination_guard", "operator_backup_or_restore_qualified",
                    "original_sqlite_access"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual((candidate["m3_2"], candidate["g2b"], candidate["writer"],
                          candidate["g2c"], candidate["real_g3"]),
                         ("IN_PROGRESS_NOT_ACCEPTED", "NOT_ACCEPTED", "NOT_PROVEN",
                          "NOT_AUTHORIZED", "STOP_UNAVAILABLE"))
        for path in (candidate["qualification"], candidate["rust_fixture"],
                     candidate["source_tests"]):
            self.assertTrue((ROOT / path).is_file())
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40338104050", doc, filename)
            self.assertIn("M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md", doc, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40338104050", doc, filename)
            self.assertIn("M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md", doc, filename)

    def test_116_pr185_terminal_and_same_profile_not_new_profile_restore_contract(self):
        terminal = self.data["post_pr185_terminal_observation"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 185)
        self.assertEqual(terminal["source_sha"], "84087eb4093b9a72b35b7ea2d6376fcce52c1ddf")
        self.assertEqual(terminal["merge_sha"], "03c205f18e4b8c7ed4780ad746d9229e7e910e2c")
        self.assertEqual(terminal["source_ci"], {"run_id": 40391038879, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40392826209, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["issue38_terminal_comment"], 6426334227)
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"]), (139, 3, 115))
        self.assertFalse(terminal["operator_backup_restore_executed"])
        self.assertFalse(terminal["m3_2_accepted"])
        candidate = self.data["next_route_c_same_profile_restore_20261026"]
        self.assertEqual(candidate["scope"], "SAME_PROFILE_RESTORE_RUNNER_ONLY")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertFalse(candidate["profile_recreation_required"])
        self.assertTrue(candidate["restored_sqlite_file_is_new"])
        self.assertTrue(candidate["previous_sqlite_file_preserved"])
        self.assertTrue(candidate["active_marker_changes_only_on_explicit_restore"])
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual((candidate["greenfield_ci_cases_expected"],
                          candidate["source_guard_cases_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (4, 6, 12))
        self.assertFalse(candidate["operator_backup_restore_qualified"])
        self.assertFalse(candidate["original_sqlite_access"])
        for path in (candidate["qualification"], candidate["rust_fixture"],
                     candidate["frontend_copy"], candidate["source_tests"]):
            self.assertTrue((ROOT / path).is_file())
        for key, expected in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE"),
                              ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)")):
            self.assertEqual(candidate[key], expected)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            s = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40392826209", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md", s, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            s = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40392826209", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md", s, name)

    def test_117_pr186_terminal_and_corrupt_same_profile_refusal_is_candidate_only(self):
        terminal = self.data["post_pr186_terminal_observation"]
        self.assertEqual(self.data["as_of"], "2026-10-27")
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 186)
        self.assertEqual(terminal["source_sha"], "ad202a0310c378bdbda430f68d9d8686f59a6e18")
        self.assertEqual(terminal["merge_sha"], "92160c6401fa8b9f2f1667704fb8f51294fdae72")
        self.assertEqual(terminal["source_ci"], {"run_id": 40402322000, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40403984550, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["issue38_terminal_comment"], 6427938179)
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"]), (140, 4, 116))
        self.assertFalse(terminal["new_operator_profile_required"])
        self.assertFalse(terminal["operator_backup_restore_executed"])
        self.assertFalse(terminal["m3_2_accepted"])
        candidate = self.data["next_route_c_same_profile_restore_refusal_20261027"]
        self.assertEqual(candidate["scope"], "SAME_PROFILE_CORRUPT_BACKUP_REFUSAL_RUNNER_ONLY")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertFalse(candidate["profile_recreation_required"])
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual((candidate["greenfield_ci_cases_expected"],
                          candidate["source_guard_cases_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (5, 7, 117, 16))
        for preserved in ("previous_sqlite_file_preserved_on_refusal",
                          "active_sqlite_file_preserved_on_refusal",
                          "activation_marker_preserved_on_refusal"):
            self.assertTrue(candidate[preserved])
        self.assertFalse(candidate["independent_operator_attestation"])
        self.assertFalse(candidate["operator_backup_restore_qualified"])
        self.assertFalse(candidate["original_sqlite_access"])
        for key, expected in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE"),
                              ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)")):
            self.assertEqual(candidate[key], expected)
        for path in (candidate["qualification"], candidate["rust_fixture"], candidate["source_tests"]):
            self.assertTrue((ROOT / path).is_file())
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            s = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40403984550", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md", s, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            s = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40403984550", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md", s, name)

    def test_118_pr187_terminal_and_logical_foreign_key_restore_refusal_candidate(self):
        terminal = self.data["post_pr187_terminal_observation"]
        self.assertEqual(self.data["as_of"], "2026-10-27")
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 187)
        self.assertEqual(terminal["source_sha"], "3029bf61d526a243a431bf2c151de0ebeaf50818")
        self.assertEqual(terminal["merge_sha"], "0b0964a723340fd832134691fdd93563c1afe9c0")
        self.assertEqual(terminal["source_ci"], {"run_id": 40444374426, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40445392523, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["issue38_terminal_comment"], 6433265532)
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"]), (141, 5, 117))
        self.assertFalse(terminal["new_operator_profile_required"])
        self.assertFalse(terminal["operator_backup_restore_executed"])
        self.assertFalse(terminal["m3_2_accepted"])
        candidate = self.data["next_route_c_same_profile_foreign_key_refusal_20261027"]
        self.assertEqual(candidate["scope"], "SAME_PROFILE_FOREIGN_KEY_INVALID_BACKUP_REFUSAL_RUNNER_ONLY")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertFalse(candidate["profile_recreation_required"])
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual((candidate["greenfield_ci_cases_expected"],
                          candidate["source_guard_cases_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (6, 8, 118, 21))
        for key in ("sqlite_integrity_check_ok_for_invalid_fixture",
                    "sqlite_foreign_key_check_rejects_invalid_fixture",
                    "previous_sqlite_file_preserved_on_refusal",
                    "active_sqlite_file_preserved_on_refusal",
                    "activation_marker_preserved_on_refusal"):
            self.assertTrue(candidate[key])
        for key in ("independent_operator_attestation", "operator_backup_restore_qualified",
                    "original_sqlite_access"):
            self.assertFalse(candidate[key])
        for key, expected in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE"),
                              ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)")):
            self.assertEqual(candidate[key], expected)
        for path in (candidate["qualification"], candidate["rust_fixture"], candidate["source_tests"]):
            self.assertTrue((ROOT / path).is_file())
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            s = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40445392523", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md", s, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            s = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40445392523", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md", s, name)

    def test_119_pr188_terminal_and_wrong_schema_restore_refusal_candidate(self):
        terminal = self.data["post_pr188_terminal_observation"]
        self.assertEqual(self.data["as_of"], "2026-10-27")
        # Historical terminal witness; the live handoff may advance beyond #188.
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 188)
        self.assertEqual(terminal["source_sha"], "9ca23c1b78c5fb2e3f49c2c3728024be374caeba")
        self.assertEqual(terminal["merge_sha"], "e4cd6ba8151f2d6cbab8723d2fb200d3ac3ffebc")
        self.assertEqual(terminal["source_ci"], {"run_id": 40450684268, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40451602743, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["issue38_terminal_comment"], 6434133177)
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"]), (142, 6, 118))
        for flag in ("new_operator_profile_required", "operator_backup_restore_executed",
                     "m3_2_accepted"):
            self.assertFalse(terminal[flag])
        candidate = self.data["next_route_c_same_profile_foreign_schema_refusal_20261027"]
        self.assertEqual(candidate["scope"], "SAME_PROFILE_WRONG_OWNER_AND_FORGED_MIGRATION_LINEAGE_RUNNER_ONLY")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertFalse(candidate["profile_recreation_required"])
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual((candidate["greenfield_ci_cases_expected"],
                          candidate["source_guard_cases_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (7, 9, 119, 27))
        for key in ("foreign_schema_owner_rejected", "forged_migration_lineage_rejected",
                    "previous_sqlite_file_preserved_on_refusal",
                    "active_sqlite_file_preserved_on_refusal",
                    "activation_marker_preserved_on_refusal"):
            self.assertTrue(candidate[key])
        for key in ("independent_operator_attestation", "operator_backup_restore_qualified",
                    "original_sqlite_access"):
            self.assertFalse(candidate[key])
        for key, expected in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE"),
                              ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)")):
            self.assertEqual(candidate[key], expected)
        for path in (candidate["qualification"], candidate["rust_fixture"], candidate["source_tests"]):
            self.assertTrue((ROOT / path).is_file())
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_HISTORY.md", "HANDOFF_PROTOCOL.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            s = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40451602743", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md", s, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            s = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40451602743", s, name)
            self.assertIn("M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md", s, name)

    def test_120_pr189_terminal_pr35_living_audit_and_prospective_boundary(self):
        terminal = self.data["post_pr189_terminal_observation"]
        audit = self.data["pr35_live_audit_prospective_fast_track_candidate_20261027"]
        self.assertEqual(self.data["as_of"], "2026-10-27")
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 189)
        self.assertEqual(terminal["source_sha"], "546cdee207e1cec049d7d0c2113696f3ce0461dd")
        self.assertEqual(terminal["merge_sha"], "009fa1723b3fc9a574e867a28759adff42e255d0")
        self.assertEqual(terminal["source_ci"], {"run_id": 40455683237, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40456835489, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["issue38_terminal_comment"], 6434867348)
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"]), (143, 7, 119))
        for flag in ("operator_backup_restore_executed", "new_operator_profile_required",
                     "m3_2_accepted"):
            self.assertFalse(terminal[flag])
        self.assertEqual(audit["scope"], "SOURCE_ONLY_PR35_AUDIT_AND_FUTURE_PROSPECTIVE_SOLO_ROUTE")
        self.assertEqual(audit["main_sha_observed"], terminal["merge_sha"])
        self.assertEqual(audit["pr35_head_sha"], "41ce7b915e76d22785d53d7fffe288d113dd0bf5")
        self.assertEqual(audit["pr35_state"], "OPEN_DRAFT_DIRTY_NOT_MERGEABLE")
        self.assertEqual((audit["pr35_commits_ahead"], audit["pr35_commits_behind"],
                          audit["pr35_changed_paths"]), (47, 645, 84))
        self.assertEqual((audit["pr35_identical_sql_paths"],
                          audit["pr35_different_existing_paths"],
                          audit["pr35_missing_in_main_paths"]), (6, 10, 68))
        self.assertTrue(audit["already_ported_rust_test_only"])
        self.assertEqual(audit["preferred_product_route"],
                         "M3_2_GREENFIELD_NEW_PROJECTS_ONLY_CANDIDATE_NOT_FORMALLY_ACCEPTED")
        self.assertFalse(audit["prospective_unblocks_m3_2_guaranteed"])
        self.assertEqual(audit["prospective_policy"],
                         "SOLO_OPERATOR_COMPENSATING_CONTROLS_POLICY_ONLY")
        self.assertEqual(audit["prospective_baseline"], "NOT_STARTED")
        self.assertEqual(audit["historical"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(audit["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(audit["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        for flag in ("profile_recreation_required", "pr35_merge_authorized",
                     "migration_007_authorized", "writer_ipc_authorized"):
            self.assertFalse(audit[flag])
        for key, expected in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE")):
            self.assertEqual(audit[key], expected)
        qualification = ROOT / audit["qualification"]
        self.assertTrue(qualification.is_file())
        self.assertIn("645 behind", qualification.read_text(encoding="utf-8"))
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40456835489", doc, name)
            self.assertIn("M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40456835489", doc, name)
            self.assertIn("M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md", doc, name)

    def test_121_pr190_terminal_and_new_only_disposable_v7_persistence_candidate(self):
        terminal = self.data["post_pr190_terminal_observation"]
        candidate = self.data["next_m32_greenfield_new_only_v7_disposable_persistence_candidate_20261027"]
        self.assertEqual(self.data["as_of"], "2026-10-27")
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 190)
        self.assertEqual(terminal["pr"], 190)
        self.assertEqual(terminal["source_sha"], "d15f58b40a8b6124967f89ffed013dab14497b13")
        self.assertEqual(terminal["merge_sha"], "7c7e02899784e52e3eb06dfff9d79a613eec95c1")
        self.assertEqual(terminal["source_ci"], {"run_id": 40461093909, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40462274918, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["issue38_terminal_comment"], 6435633242)
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(candidate["scope"], "TEST_ONLY_DISPOSABLE_SQLITE_V7_NEW_PROJECT_CHRONOLOGY_CLOSE_REOPEN")
        self.assertEqual(candidate["rust_test_name"],
                         "m32_new_only_disposable_v7_chronology_survives_reopen_without_touching_prior_v6")
        self.assertEqual((candidate["rust_base_tests_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (144, 121, 16))
        for flag in ("new_disposable_file_reopened", "separate_prior_v6_bytes_preserved",
                     "sqlite_integrity_and_foreign_keys_checked", "cycle_and_cross_universe_refused",
                     "immutable_anchor_correction_persisted"):
            self.assertTrue(candidate[flag], flag)
        for flag in ("operator_sqlite_access", "production_v7_opener_authorized",
                     "migration_007_authorized", "writer_ipc_authorized",
                     "new_operator_profile_required", "independent_operator_attestation"):
            self.assertFalse(candidate[flag], flag)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, expected in (("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                              ("prospective", "NOT_STARTED"),
                              ("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE")):
            self.assertEqual(candidate[key], expected)
        self.assertIn(candidate["rust_test_name"],
                      (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8"))
        self.assertTrue((ROOT / candidate["qualification"]).is_file())
        self.assertTrue((ROOT / candidate["sqlite_inventory"]).is_file())
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40462274918", doc, name)
            self.assertIn("M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40462274918", doc, name)
            self.assertIn("M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md", doc, name)

    def test_122_pr191_terminal_and_exclusive_new_only_file_claim_candidate(self):
        terminal = self.data["post_pr191_terminal_observation"]
        candidate = self.data["next_m32_greenfield_v7_exclusive_new_file_claim_candidate_20261027"]
        self.assertEqual(self.data["as_of"], "2026-10-27")
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 191)
        self.assertEqual(terminal["pr"], 191)
        self.assertEqual(terminal["source_sha"], "c6b23ae071392c5f68912e53915df5067787605b")
        self.assertEqual(terminal["source_ci"], {"run_id": 40469481613, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "2b4a7aaa37b2ada590a8e05fc4c5e973949041cc")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40470700689, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"], terminal["sqlite_inventory_tests"]),
                         (144, 7, 121, 25))
        self.assertEqual(terminal["issue38_terminal_comment"], 6436913166)
        for flag in ("operator_backup_restore_executed", "new_operator_profile_required",
                     "m3_2_accepted"):
            self.assertFalse(terminal[flag])
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(candidate["scope"], "TEST_ONLY_DISPOSABLE_EXCLUSIVE_OS_CREATE_NEW_THEN_SQLITE_V7")
        self.assertEqual((candidate["rust_base_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (147, 28, 122, 18))
        for flag in ("os_create_new_exclusive_test_only",
                     "existing_v6_and_arbitrary_file_bytes_preserved",
                     "existing_directory_and_uncreated_parent_refused",
                     "orphan_wal_shm_journal_refused_and_preserved",
                     "only_one_concurrent_creator_accepted",
                     "test_only_v7_reopens_without_second_ownership_claim"):
            self.assertTrue(candidate[flag], flag)
        for flag in ("operator_sqlite_access", "production_v7_opener_authorized",
                     "adversarial_path_substitution_proven_resistant",
                     "migration_007_authorized", "writer_ipc_authorized",
                     "new_operator_profile_required", "independent_operator_attestation"):
            self.assertFalse(candidate[flag], flag)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, expected in (("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                              ("prospective", "NOT_STARTED"),
                              ("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE")):
            self.assertEqual(candidate[key], expected)
        self.assertTrue((ROOT / candidate["qualification"]).is_file())
        self.assertTrue((ROOT / candidate["sqlite_inventory"]).is_file())
        self.assertTrue((ROOT / candidate["source_tests"]).is_file())
        source = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        for name in ("open_new_only_disposable_file", "m32_new_only_claim_refuses_existing_file_directory_and_orphan_sidecars",
                     "m32_exclusive_new_file_claim_builds_test_only_v7_and_reopen_cannot_reclaim_it",
                     "m32_exclusive_claim_two_concurrent_creators_only_one_wins"):
            self.assertIn(name, source)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40470700689", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40470700689", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md", doc, name)

    def test_123_pr192_terminal_and_pinned_handoff_parent_swap_candidate(self):
        terminal = self.data["post_pr192_terminal_observation"]
        candidate = self.data["next_m32_greenfield_v7_pinned_handoff_parent_namespace_candidate_20261027"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 192)
        self.assertEqual(terminal["pr"], 192)
        self.assertEqual(terminal["source_sha"], "a061311a4d8ca54b213d134c2affa34defa3f023")
        self.assertEqual(terminal["source_ci"], {"run_id": 40474849956, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "0584291d6dc3c8d2fc8860c8c5084250f4c43ba4")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40476232974, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"], terminal["sqlite_inventory_tests"]),
                         (147, 7, 122, 28))
        self.assertEqual(terminal["issue38_terminal_comment"], 6437767007)
        for flag in ("production_v7_opener_qualified",
                     "adversarial_path_substitution_resistance_proven",
                     "operator_backup_restore_executed", "m3_2_accepted"):
            self.assertFalse(terminal[flag])
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]), (149, 30, 123, 18))
        for flag in ("windows_held_os_claim_while_sqlite_opens_test_only",
                     "windows_immediate_parent_no_delete_share_test_only",
                     "parent_namespace_swap_negative_witness"):
            self.assertTrue(candidate[flag], flag)
        for flag in ("full_ancestor_identity_and_acl_verified",
                     "adversarial_path_substitution_proven_resistant",
                     "production_v7_opener_authorized", "operator_sqlite_access",
                     "new_operator_profile_required", "migration_007_authorized",
                     "writer_ipc_authorized", "independent_operator_attestation"):
            self.assertFalse(candidate[flag], flag)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, expected in (("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                              ("prospective", "NOT_STARTED"),
                              ("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE")):
            self.assertEqual(candidate[key], expected)
        self.assertTrue((ROOT / candidate["qualification"]).is_file())
        self.assertTrue((ROOT / candidate["rust_fixture"]).is_file())
        self.assertTrue((ROOT / candidate["sqlite_inventory_tests_file"]).is_file())
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40476232974", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40476232974", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md", doc, name)

    def test_124_pr193_terminal_and_owned_fixture_directory_chain_candidate(self):
        terminal = self.data["post_pr193_terminal_observation"]
        candidate = self.data["next_m32_greenfield_v7_owned_fixture_directory_chain_candidate_20261027"]
        self.assertGreaterEqual(self.data["last_confirmed_merged_pr"], 193)
        self.assertEqual(self.data["last_verified_pr_head"],
                         self.data["post_pr197_terminal_observation"]["source_sha"])
        self.assertEqual(self.data["last_confirmed_main_before_handoff"],
                         self.data["post_pr197_terminal_observation"]["merge_sha"])
        self.assertEqual(self.data["last_verified_ci"]["run_id"], 40556607820)
        self.assertEqual(terminal["pr"], 193)
        self.assertEqual(terminal["source_sha"], "38540a4602c5c5e4f9d9b3bdb6b8bf155e0ed256")
        self.assertEqual(terminal["source_ci"], {"run_id": 40485043798, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "8d034d66c3de76735c356c6f79e436c0b9965dec")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40486676658, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["handoff_tests"], terminal["sqlite_inventory_tests"]),
                         (149, 7, 123, 30))
        self.assertEqual(terminal["issue38_terminal_comment"], 6439378032)
        for flag in ("production_v7_opener_qualified", "full_ancestor_identity_proven",
                     "sqlite_vfs_os_handle_binding_proven", "m3_2_accepted"):
            self.assertFalse(terminal[flag], flag)
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"],
                          candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"],
                          candidate["handoff_tests_expected"],
                          candidate["sqlite_test_open_occurrences_expected"]),
                         (151, 7, 32, 124, 18))
        for flag in ("lexical_escape_and_unsafe_filename_refusal_test_only",
                     "windows_pinned_fixture_directory_chain_test_only",
                     "windows_fixture_volume_and_fileindex_compared_test_only",
                     "windows_reparse_attribute_veto_test_only"):
            self.assertTrue(candidate[flag], flag)
        for flag in ("all_absolute_ancestors_above_fixture_root_proven",
                     "operator_profile_root_acl_and_junctions_proven",
                     "sqlite_vfs_os_handle_binding_proven",
                     "adversarial_substitution_resistance_proven",
                     "operator_sqlite_access", "production_v7_opener_authorized",
                     "new_operator_profile_required", "migration_007_authorized",
                     "writer_ipc_authorized", "independent_operator_attestation"):
            self.assertFalse(candidate[flag], flag)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, expected in (("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                              ("prospective", "NOT_STARTED"),
                              ("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE")):
            self.assertEqual(candidate[key], expected)
        self.assertTrue((ROOT / candidate["qualification"]).is_file())
        self.assertTrue((ROOT / candidate["rust_fixture"]).is_file())
        self.assertTrue((ROOT / candidate["sqlite_inventory_tests_file"]).is_file())
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40486676658", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40486676658", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md", doc, name)

    def test_125_pr194_negative_win32_runs_and_bounded_revalidation_candidate(self):
        event = self.data["pr194_windows_negative_and_revalidation_candidate_20261027"]
        self.assertEqual(event["pr"], 194)
        self.assertEqual(event["state_at_checkpoint"], "OPEN_NOT_MERGED")
        self.assertEqual(event["base_main_sha"], "8d034d66c3de76735c356c6f79e436c0b9965dec")
        attempts = event["source_attempts"]
        self.assertEqual([a["run_id"] for a in attempts],
                         [40498356467, 40499869627, 40501278786])
        self.assertTrue(all(a["conclusion"] == "FAILURE" for a in attempts))
        self.assertEqual([(a["rust_passed"], a["rust_failed"]) for a in attempts[1:]],
                         [(150, 1), (150, 1)])
        self.assertEqual(event["issue38_terminal_stop_comment"], 6441614257)
        self.assertEqual((event["rust_tests_expected"], event["inventory_guards_expected"],
                          event["continuity_contracts_expected"]), (151, 32, 125))
        self.assertTrue(event["windows_same_name_substitution_refusal_test_only"])
        self.assertTrue(event["independent_pristine_new_only_sqlite_fixture_test_only"])
        for field in ("new_candidate_source_ci_qualified", "directory_rename_prevention_proven",
                      "post_revalidation_race_eliminated", "operator_root_and_above_ancestors_proven",
                      "sqlite_vfs_os_handle_binding_proven", "m3_2_accepted"):
            self.assertFalse(event[field], field)
        self.assertEqual(event["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(event["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        src = (ROOT / event["rust_fixture"]).read_text(encoding="utf-8")
        self.assertIn("fn revalidate_checked_fixture_chain", src)
        self.assertIn("m32_windows_owned_fixture_chain_rechecks_substitution_before_sqlite", src)
        self.assertIn("fs::create_dir(&second)", src)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40501278786", doc, name)
            self.assertIn("NON QUALIFI", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            self.assertIn("40501278786", (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8"))

    def test_126_pr194_terminal_and_native_sqlite_windows_handle_postopen_candidate(self):
        terminal = self.data["post_pr194_terminal_observation"]
        self.assertEqual(terminal["pr"], 194)
        self.assertEqual(terminal["source_sha"], "de54c003421d09309f5bff8a31d110fb24d93678")
        self.assertEqual(terminal["source_ci"], {"run_id": 40507105063, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "567638515444d621749507f9700a3e2a69c52c6b")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40508416842, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["sqlite_inventory_tests"],
                          terminal["handoff_tests"]), (151, 32, 125))
        self.assertEqual(terminal["issue38_terminal_comment"], 6442750005)
        self.assertTrue(terminal["windows_prior_name_swap_revalidation_test_only"])
        for key in ("windows_empty_directory_name_pin_proven", "post_revalidation_race_eliminated",
                    "sqlite_vfs_native_handle_identity_proven", "production_v7_opener_authorized",
                    "m3_2_accepted"):
            self.assertFalse(terminal[key], key)

        candidate = self.data["next_m32_sqlite_windows_native_handle_postopen_candidate_20261027"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"], candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"], candidate["handoff_tests_expected"]),
                         (153, 7, 34, 126))
        self.assertEqual(candidate["sqlite_test_open_occurrences_expected"], 19)
        self.assertTrue(candidate["file_claim_to_sqlite_handle_comparison_test_only"])
        self.assertTrue(candidate["post_precheck_file_name_swap_refusal_test_only"])
        for key in ("new_candidate_source_ci_qualified", "win32_fileid_128_proven",
                    "pre_xopen_identity_binding_proven", "atomic_sqlite_vfs_handoff_proven",
                    "post_xopen_side_effects_ruled_out", "all_operator_ancestors_acl_reparse_proven",
                    "operator_sqlite_access", "production_v7_opener_authorized",
                    "new_operator_profile_required", "migration_007_authorized", "writer_ipc_authorized",
                    "independent_operator_attestation"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)
        self.assertTrue((ROOT / candidate["qualification"]).is_file())
        fixture = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        self.assertIn("SQLITE_FCNTL_WIN32_GET_HANDLE", fixture)
        self.assertIn("m32_windows_sqlite_vfs_native_handle_detects_post_check_name_substitution", fixture)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40508416842", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md", doc, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40508416842", doc, name)
            self.assertIn("M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md", doc, name)

    def test_127_pr195_terminal_fileid128_and_hello_auth_boundary_is_separate(self):
        terminal = self.data["post_pr195_terminal_observation"]
        self.assertEqual(terminal["pr"], 195)
        self.assertEqual(terminal["source_sha"], "f84f3035170baa4830879796230675ad8b328a2c")
        self.assertEqual(terminal["source_ci"], {"run_id": 40516204731, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "1ab320f7834086ac587ce2fdaa8638d7c29d61f5")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40518270685, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["sqlite_inventory_tests"], terminal["handoff_tests"]),
                         (153, 7, 34, 126))
        self.assertEqual(terminal["issue38_terminal_comment"], 6444458042)
        self.assertTrue(terminal["win32_vfs_handle_compare_post_xopen_test_only"])
        for key in ("atomic_sqlite_vfs_handoff_proven", "pre_xopen_side_effects_ruled_out",
                    "win32_fileid_128_proven", "production_v7_opener_authorized",
                    "windows_hello_auth_implemented", "m3_2_accepted"):
            self.assertFalse(terminal[key], key)

        candidate = self.data["next_m32_win32_fileid128_and_hello_boundary_candidate_20261027"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"], candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"], candidate["handoff_tests_expected"]),
                         (154, 7, 35, 127))
        self.assertEqual(candidate["sqlite_test_open_occurrences_expected"], 20)
        for key in ("win32_fileidinfo_128_claim_and_vfs_fixture_test_only",
                    "win32_fileid128_post_swap_observation_test_only",
                    "windows_hello_evaluation_document_only"):
            self.assertTrue(candidate[key], key)
        for key in ("new_candidate_source_ci_qualified", "windows_hello_userconsent_implemented",
                    "webauthn_account_implemented", "app_username_password_created",
                    "pin_collected_or_stored", "atomic_sqlite_vfs_handoff_proven",
                    "pre_xopen_identity_binding_proven", "same_user_external_writer_absence_proven",
                    "operator_ancestors_sidecars_acl_proven", "operator_sqlite_access",
                    "production_v7_opener_authorized", "new_operator_profile_required",
                    "migration_007_authorized", "writer_ipc_authorized",
                    "independent_operator_attestation"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)
        self.assertTrue((ROOT / candidate["qualification"]).is_file())
        fixture = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        self.assertIn("GetFileInformationByHandleEx", fixture)
        self.assertIn("m32_windows_sqlite_fileid_128_matches_claim_but_cannot_prevent_prior_swap", fixture)
        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        for signal in ("UserConsentVerifier", "RequestVerificationForWindowAsync", "WebAuthn",
                       "PIN", "NON PROUVÉS", "xOpen"):
            self.assertIn(signal, doc)
        for name in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            content = (DIRECTORY / name).read_text(encoding="utf-8")
            self.assertIn("40518270685", content, name)
            self.assertIn("M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md", content, name)
        for name in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            content = (ROOT / "docs/roadmap" / name).read_text(encoding="utf-8")
            self.assertIn("40518270685", content, name)
            self.assertIn("M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md", content, name)

    def test_128_pr196_terminal_single_user_hello_consent_policy_candidate_only(self):
        terminal = self.data["post_pr196_terminal_observation"]
        self.assertEqual(terminal["pr"], 196)
        self.assertEqual(terminal["source_sha"], "2925a6a561f54fe3e7c0dc9aa7301e6a1c55930a")
        self.assertEqual(terminal["source_ci"], {"run_id": 40523209147, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "3546e62a19cb4db0da970cb07019982ff6c8634a")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40525427034, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["sqlite_inventory_tests"], terminal["handoff_tests"]),
                         (154, 7, 35, 127))
        self.assertEqual(terminal["issue38_terminal_comment"], 6445506535)
        self.assertTrue(terminal["win32_fileid_128_test_only"])
        self.assertFalse(terminal["pre_xopen_atomic_identity_proven"])
        self.assertFalse(terminal["windows_hello_userconsent_implemented"])

        candidate = self.data["next_m32_single_user_windows_hello_consent_policy_candidate_20261027"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(candidate["owner_product_decision"],
                         "SINGLE_WINDOWS_USER_WINDOWS_HELLO_FOR_SENSITIVE_OPERATIONS_ONLY")
        self.assertEqual((candidate["rust_base_tests_expected"],
                          candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"],
                          candidate["handoff_tests_expected"]), (165, 7, 36, 128))
        for flag in ("one_shot_action_target_revision_bound_test_only",
                     "cancel_unavailable_expired_replay_or_changed_intent_refusal_test_only",
                     "separate_gate_and_fresh_preflight_required_test_only"):
            self.assertTrue(candidate[flag], flag)
        for flag in ("candidate_ci_qualified", "new_user_accounts_requested",
                     "new_username_password_requested", "windows_hello_native_interop_implemented",
                     "windows_hello_dialog_activated", "production_sensitive_action_guard_implemented",
                     "app_pin_collected_or_stored", "app_username_password_created",
                     "atomic_sqlite_vfs_handoff_proven", "writer_absence_proven", "operator_sqlite_access",
                     "production_v7_opener_authorized", "new_operator_profile_required",
                     "migration_007_authorized", "writer_ipc_authorized",
                     "independent_operator_attestation"):
            self.assertFalse(candidate[flag], flag)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)
        qualification = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        for signal in ("mono-utilisateur", "Windows Hello", "RequestVerificationForWindowAsync",
                       "AUCUN", "xOpen", "NON QUALIFIÉ"):
            self.assertIn(signal, qualification)
        rust = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        self.assertIn("fn m32_hello_fixture_exact_verified_decision_is_one_shot", rust)
        self.assertIn("fn m32_hello_fixture_backend_revalidation_still_required_after_hello", rust)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            doc = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40525427034", doc, filename)
            self.assertIn("M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md", doc, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            doc = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40525427034", doc, filename)
            self.assertIn("M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md", doc, filename)

    def test_129_pr197_terminal_hello_policy_and_live_continuity_refresh(self):
        terminal = self.data["post_pr197_terminal_observation"]
        self.assertEqual(terminal["pr"], 197)
        self.assertEqual(terminal["source_sha"], "ab55f506f767f36659ffdd50c2970d9c703e0f0b")
        self.assertEqual(terminal["source_ci"], {"run_id": 40556607820, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "dde962a50e3a063753fb77e9a5bcee014f406d30")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40558476584, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["sqlite_inventory_tests"], terminal["handoff_tests"]),
                         (165, 7, 36, 128))
        self.assertEqual(terminal["issue38_terminal_comment"], 6450320382)
        self.assertTrue(terminal["github_required_check_success"])
        self.assertTrue(terminal["single_windows_user_hello_only_product_decision"])
        self.assertTrue(terminal["one_shot_sensitive_consent_policy_rust_cfg_test_only"])
        for flag in ("native_windows_hello_userconsent_implemented", "windows_hello_dialog_run",
                     "app_pin_or_password_collected", "new_app_accounts_implemented",
                     "production_sensitive_action_guard_implemented", "atomic_sqlite_pre_xopen_proven",
                     "writer_absence_proven", "m3_2_accepted"):
            self.assertFalse(terminal[flag], flag)
        self.assertEqual(terminal["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(self.data["last_confirmed_merged_pr"], 197)
        self.assertEqual(self.data["last_verified_pr_head"], terminal["source_sha"])
        self.assertEqual(self.data["last_confirmed_main_before_handoff"], terminal["merge_sha"])
        self.assertEqual(self.data["last_verified_ci"], {
            "run_id": 40556607820,
            "context": "Windows frontend and Rust checks",
            "conclusion": "SUCCESS", "source": "PR197_EXACT_HEAD"})

        followup = self.data["next_m32_pr197_terminal_continuity_sync_candidate_20261027"]
        self.assertEqual(followup["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((followup["rust_base_tests_expected_unchanged"],
                          followup["greenfield_runner_tests_expected_unchanged"],
                          followup["sqlite_inventory_tests_expected_unchanged"],
                          followup["handoff_tests_expected"]), (165, 7, 36, 129))
        self.assertEqual(followup["scope"],
                         "DOCUMENTATION_ONLY_PR197_TERMINAL_REVALIDATION_NO_RUNTIME_OR_OPERATOR_ACTION")
        for flag in ("new_candidate_source_ci_qualified", "native_windows_hello_implemented",
                     "operator_access", "new_operator_profile_required", "migration_007_authorized",
                     "writer_ipc_authorized", "pr35_merge_authorized"):
            self.assertFalse(followup[flag], flag)
        self.assertEqual(followup["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        for key, expected in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"),
                              ("g2b", "NOT_ACCEPTED"), ("writer", "NOT_PROVEN"),
                              ("g2c", "NOT_AUTHORIZED"), ("real_g3", "STOP_UNAVAILABLE"),
                              ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                              ("prospective", "NOT_STARTED")):
            self.assertEqual(followup[key], expected)

        for file in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                     "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                     "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            source = (DIRECTORY / file).read_text(encoding="utf-8")
            self.assertIn("40558476584", source, file)
            self.assertIn("dde962a50e3a063753fb77e9a5bcee014f406d30", source, file)
            self.assertIn("M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md",
                          source, file)
        for file in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            source = (ROOT / "docs/roadmap" / file).read_text(encoding="utf-8")
            self.assertIn("40558476584", source, file)
            self.assertIn("dde962a50e3a063753fb77e9a5bcee014f406d30", source, file)
        short_bytes = (DIRECTORY / "RESUME_PROMPT_SHORT.md").read_bytes()
        self.assertLess(len(short_bytes), 4200)
        # A Windows checkout may use CRLF: reserve one extra byte per line.
        self.assertLess(len(short_bytes.replace(b"\r\n", b"\n")) +
                        short_bytes.count(b"\n"), 4200)

    def test_130_pr198_terminal_desktop_hello_hwnd_source_only_candidate(self):
        terminal = self.data["post_pr198_terminal_observation"]
        self.assertEqual(terminal["pr"], 198)
        self.assertEqual(terminal["source_sha"], "9b4b4049c461986c8427620f649a4e2113078800")
        self.assertEqual(terminal["source_ci"], {"run_id": 40569850503, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "34b4174dd79d7c133b3700d72a705236f7623640")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40571697037, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["sqlite_inventory_tests"], terminal["handoff_tests"]),
                         (165, 7, 36, 129))
        self.assertEqual(terminal["issue38_terminal_comment"], 6452075388)
        self.assertTrue(terminal["protect_main_active_strict"])
        self.assertEqual(terminal["operator_execution"], "NO_OPERATOR_EXECUTION")

        candidate = self.data["next_m32_desktop_hello_hwnd_source_candidate_20261027"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"],
                          candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"],
                          candidate["handoff_tests_expected"]), (171, 7, 36, 130))
        self.assertEqual(candidate["desktop_interop_min_windows_build"], 22000)
        self.assertTrue(candidate["synthetic_windows10_no_uwp_fallback"])
        self.assertTrue(candidate["synthetic_hwnd_ownership_and_window_swap_refusals"])
        for key in ("candidate_ci_qualified", "native_windows_hello_implemented",
                    "native_hwnd_validation_proven", "trusted_backend_sensitive_action_guard_implemented",
                    "app_pin_or_password_collected", "new_app_accounts_implemented",
                    "atomic_sqlite_pre_xopen_proven", "writer_absence_proven", "operator_sqlite_access",
                    "production_v7_opener_authorized", "new_operator_profile_required",
                    "migration_007_authorized", "writer_ipc_authorized",
                    "independent_operator_attestation"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)

        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        for signal in ("Windows build 22000", "Windows 10", "RequestVerificationForWindowAsync",
                       "backend", "xOpen", "NON QUALIFIÉ", "171 Rust", "130 contrats"):
            self.assertIn(signal, doc)
        rust = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        lib = (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8")
        self.assertIn("#[cfg(test)]\nmod m32_desktop_hello_boundary_tests;", lib)
        self.assertEqual(rust.count("    #[test]"), 6)
        for test_name in ("m32_desktop_hello_fixture_windows_10_never_falls_back_to_uwp",
                          "m32_desktop_hello_fixture_22000_is_only_a_call_candidate",
                          "m32_desktop_hello_fixture_gate_must_precede_even_eligibility",
                          "m32_desktop_hello_fixture_missing_foreign_or_inactive_window_refused",
                          "m32_desktop_hello_fixture_all_unavailable_states_refused",
                          "m32_desktop_hello_fixture_snapshot_swap_and_stale_completion_refused"):
            self.assertIn("fn " + test_name, rust)
        for forbidden in ("#[tauri::command]", "Connection::open", "unsafe {",
                          "windows::", "winapi::", "RequestVerificationForWindowAsync(",
                          "tauri::", "std::fs::"):
            self.assertNotIn(forbidden, rust, forbidden)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40571697037", body, filename)
            self.assertIn("M3_2_WINDOWS_HELLO_DESKTOP_HWND_BACKEND_BOUNDARY_20261027.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40571697037", body, filename)
            self.assertIn("M3_2_WINDOWS_HELLO_DESKTOP_HWND_BACKEND_BOUNDARY_20261027.md", body, filename)

    def test_131_pr199_terminal_and_windows_vfs_predispatch_refusal_candidate(self):
        terminal = self.data["post_pr199_terminal_observation"]
        self.assertEqual(terminal["pr"], 199)
        self.assertEqual(terminal["source_sha"], "debc6f9cea8ba668f64afd9c815445c282c842c4")
        self.assertEqual(terminal["source_ci"], {"run_id": 40576413834, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "4e04412b1d4cbdb4ce738b32c8a06c2ab6127b61")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40578342548, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["sqlite_inventory_tests"], terminal["handoff_tests"]),
                         (171, 7, 36, 130))
        self.assertEqual(terminal["issue38_terminal_comment"], 6453334855)
        self.assertTrue(terminal["protect_main_active_strict"])
        self.assertEqual(terminal["operator_execution"], "NO_OPERATOR_EXECUTION")

        candidate = self.data["next_m32_sqlite_predelegate_vfs_source_candidate_20261027"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"], candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"], candidate["handoff_tests_expected"]),
                         (174, 7, 37, 131))
        self.assertTrue(candidate["vfs_registration_test_only"])
        self.assertTrue(candidate["named_vfs_never_default"])
        self.assertTrue(candidate["main_and_journal_predispatch_refusals_expected"])
        for key in ("candidate_ci_qualified", "production_v7_opener_implemented",
                    "atomic_sqlite_pre_xopen_proven", "writer_absence_proven",
                    "native_hello_authorized", "operator_sqlite_access", "new_operator_profile_required",
                    "migration_007_authorized", "writer_ipc_authorized",
                    "independent_operator_attestation"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)
        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        fixture = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        for keyword in ("NON QUALIFIÉE", "xOpen", "avant délégation", "174 Rust",
                        "131 contrats", "PAS un ouvreur v7 atomique", "writer"):
            self.assertIn(keyword, doc)
        # The PR200 baseline had three tests; subsequent fixture-only witnesses
        # may extend this module without changing the prior terminal result.
        self.assertGreaterEqual(fixture.count("#[test]"), 3)
        self.assertIn("sqlite3_vfs_register", fixture)
        self.assertIn("sqlite3_vfs_unregister", fixture)
        self.assertIn("SQLITE_OPEN_MAIN_JOURNAL", fixture)
        self.assertIn("SQLITE_OPEN_MAIN_DB", fixture)
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_sqlite_vfs_preopen_tests;",
                      (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8"))
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40578342548", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_PREDELEGATION_REFUSAL_FIXTURE_20261027.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40578342548", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_PREDELEGATION_REFUSAL_FIXTURE_20261027.md", body, filename)

    def test_132_pr200_terminal_and_vfs_fileid128_callback_toctou_candidate(self):
        terminal = self.data["post_pr200_terminal_observation"]
        self.assertEqual(terminal["pr"], 200)
        self.assertEqual(terminal["source_sha"], "6b9ff6351ab5e74661a65fa5b8d895237fc6d4bc")
        self.assertEqual(terminal["source_ci"], {"run_id": 40584565021, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "beda84001ebe6ee2769cb9377017848e52319e70")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40586436340, "conclusion": "SUCCESS"})
        self.assertEqual((terminal["rust_base_tests"], terminal["greenfield_runner_tests"],
                          terminal["sqlite_inventory_tests"], terminal["handoff_tests"]),
                         (174, 7, 37, 131))
        self.assertEqual((terminal["issue38_source_comment"], terminal["issue38_terminal_comment"]),
                         (6453910958, 6454165007))
        self.assertTrue(terminal["protect_main_active_strict"])
        self.assertEqual(terminal["operator_execution"], "NO_OPERATOR_EXECUTION")

        candidate = self.data["next_m32_vfs_fileid128_predelegate_toctou_candidate_20261027"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual((candidate["rust_base_tests_expected"], candidate["greenfield_runner_tests_expected"],
                          candidate["sqlite_inventory_tests_expected"], candidate["handoff_tests_expected"]),
                         (177, 7, 38, 132))
        self.assertTrue(candidate["fileid128_precheck_inside_vfs_callback"])
        self.assertTrue(candidate["deliberate_post_precheck_swap_counterexample"])
        for key in ("candidate_ci_qualified", "production_v7_opener_implemented",
                    "atomic_sqlite_pre_xopen_proven", "writer_absence_proven", "native_hello_authorized",
                    "operator_sqlite_access", "new_operator_profile_required", "migration_007_authorized",
                    "writer_ipc_authorized", "independent_operator_attestation"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)
        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        fixture = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        for keyword in ("NON QUALIFIÉE", "FileId128", "xOpen", "177 tests Rust",
                        "132 contrats", "fenêtre", "writer"):
            self.assertIn(keyword, doc)
        self.assertGreaterEqual(fixture.count("#[test]"), 6)
        for signal in ("GetFileInformationByHandleEx", "SQLITE_FCNTL_WIN32_GET_HANDLE",
                       "FileIdPrecheckPlan", "swaps_after_precheck",
                       "m32_vfs_fixture_fileid128_precheck_accepts_stable_disposable_identity",
                       "m32_vfs_fixture_fileid128_precheck_refuses_already_replaced_name",
                       "m32_vfs_fixture_fileid128_precheck_then_internal_name_swap_is_not_atomic"):
            self.assertIn(signal, fixture)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40586436340", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_FILEID128_PREDISPATCH_TOCTOU_20261027.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40586436340", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_FILEID128_PREDISPATCH_TOCTOU_20261027.md", body, filename)

    def test_133_pr201_terminal_and_wal_shm_split_test_only_candidate(self):
        terminal = self.data["post_pr201_terminal_observation"]
        self.assertEqual(terminal["pr"], 201)
        self.assertEqual(terminal["source_sha"], "c9b8567f6b1a0c4af44a835ec2fe5f39449193e5")
        self.assertEqual(terminal["source_ci"], {"run_id": 40593808508, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "d235e492c5081734ff226563eec6fdb983e4808d")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40595455638, "conclusion": "SUCCESS"})
        self.assertEqual(tuple(terminal[key] for key in ("rust_base_tests", "greenfield_runner_tests",
                                                  "sqlite_inventory_tests", "handoff_tests")),
                         (177, 7, 38, 132))
        self.assertEqual(terminal["issue38_terminal_comment"], 6455411875)
        self.assertTrue(terminal["protect_main_active_strict"])
        candidate = self.data["next_m32_vfs_wal_shm_boundary_candidate_20261028"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(tuple(candidate[key] for key in ("rust_base_tests_expected",
            "greenfield_runner_tests_expected", "sqlite_inventory_tests_expected",
            "handoff_tests_expected")), (179, 7, 39, 133))
        for key in ("candidate_ci_qualified", "production_v7_opener_implemented",
            "atomic_sqlite_pre_xopen_proven", "writer_absence_proven", "operator_sqlite_access",
            "native_hello_authorized", "migration_007_authorized", "writer_ipc_authorized"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["real_g3"], "STOP_UNAVAILABLE")
        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        for signal in ("NON QUALIFIÉE", "SQLITE_OPEN_WAL", "xShmMap", "-shm",
                       "179 Rust", "133 contrats", "writer"):
            self.assertIn(signal, doc)
        fixture = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        self.assertGreaterEqual(fixture.count("#[test]"), 8)
        self.assertIn("SQLITE_OPEN_WAL", fixture)
        self.assertIn("xShmMap", fixture)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40595455638", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_WAL_SHM_BOUNDARY_20261028.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40595455638", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_WAL_SHM_BOUNDARY_20261028.md", body, filename)

    def test_134_pr202_terminal_and_xshmmap_wrapper_fixture_candidate(self):
        terminal = self.data["post_pr202_terminal_observation"]
        self.assertEqual(terminal["pr"], 202)
        self.assertEqual(terminal["source_sha"], "8288c26c1ca7c4477c86d1a51713e931751f6b8a")
        self.assertEqual(terminal["source_ci"], {"run_id": 40609906017, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "60ca76331d45062317cf2b4794a06733becca1d7")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40611263489, "conclusion": "SUCCESS"})
        self.assertEqual(tuple(terminal[key] for key in ("rust_base_tests", "greenfield_runner_tests",
                                                  "sqlite_inventory_tests", "handoff_tests")),
                         (179, 7, 39, 133))
        self.assertEqual(terminal["issue38_terminal_comment"], 6457823553)
        self.assertTrue(terminal["protect_main_active_strict"])
        candidate = self.data["next_m32_vfs_shm_methods_wrapper_candidate_20261028"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(tuple(candidate[key] for key in ("rust_base_tests_expected",
            "greenfield_runner_tests_expected", "sqlite_inventory_tests_expected",
            "handoff_tests_expected")), (181, 7, 40, 134))
        for key in ("candidate_ci_qualified", "production_v7_opener_implemented",
            "atomic_sqlite_pre_xopen_proven", "writer_absence_proven", "operator_sqlite_access",
            "native_hello_authorized", "migration_007_authorized", "writer_ipc_authorized"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(candidate["real_g3"], "STOP_UNAVAILABLE")
        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        for signal in ("NON QUALIFIÉE", "xShmMap", "io_methods", "181 Rust", "134 contrats",
                       "writer", "szOsFile"):
            self.assertIn(signal, doc)
        fixture = (ROOT / candidate["rust_fixture"]).read_text(encoding="utf-8")
        self.assertEqual(fixture.count("#[test]"), 12)
        self.assertIn("fixture_xshm_map", fixture)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40611263489", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_SHM_IO_METHODS_WRAPPER_20261028.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40611263489", body, filename)
            self.assertIn("M3_2_SQLITE_VFS_SHM_IO_METHODS_WRAPPER_20261028.md", body, filename)
    def test_135_pr203_terminal_and_unwired_single_owner_writer_candidate(self):
        terminal = self.data["post_pr203_terminal_observation"]
        self.assertEqual(terminal["pr"], 203)
        self.assertEqual(terminal["source_sha"], "9ec042bd57d6633d5aa9df8ca0a4a3530e83c2df")
        self.assertEqual(terminal["source_ci"], {"run_id": 40646300928, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "17bf8e8456c4f06875141788b30fcaa1d7f4a975")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40647564175, "conclusion": "SUCCESS"})
        self.assertEqual(tuple(terminal[key] for key in ("rust_base_tests", "greenfield_runner_tests",
                                                    "sqlite_inventory_tests", "handoff_tests")),
                         (181, 7, 40, 134))
        self.assertEqual(terminal["issue38_terminal_comment"], 6463052495)
        self.assertTrue(terminal["protect_main_active_strict"])
        candidate = self.data["next_m32_v7_single_owner_writer_preparation_candidate_20261028"]
        self.assertEqual(candidate["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(tuple(candidate[key] for key in ("rust_base_tests_expected",
            "greenfield_runner_tests_expected", "sqlite_inventory_tests_expected",
            "handoff_tests_expected")), (189, 7, 41, 135))
        self.assertTrue(candidate["prepared_rust_writer_module_in_backend_source"])
        for key in ("candidate_ci_qualified", "production_v7_opener_implemented",
            "runtime_admission_token_available", "tauri_state_registered", "writer_ipc_authorized",
            "atomic_sqlite_pre_xopen_proven", "writer_absence_proven", "operator_sqlite_access",
            "native_hello_authorized", "migration_007_authorized"):
            self.assertFalse(candidate[key], key)
        self.assertEqual(candidate["operator_execution"], "NO_OPERATOR_EXECUTION")
        self.assertEqual(candidate["profile_identifier"], "com.fabulaxiom.greenfield.v1")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(candidate[key], value)
        doc = (ROOT / candidate["qualification"]).read_text(encoding="utf-8")
        fixture = (ROOT / candidate["rust_module"]).read_text(encoding="utf-8")
        for term in ("NON QUALIFIÉE", "189 Rust", "135 contrats", "writer", "Tauri"):
            self.assertIn(term, doc)
        self.assertEqual(fixture.count("#[test]"), 8)
        for term in ("sync_channel(QUEUE_CAPACITY)", "TransactionBehavior::Immediate",
                     "set_transaction_behavior", "V7WriterAdmission", "#[cfg(test)]",
                     "fn worker_loop", "WriterError::AdmissionRejected"):
            self.assertIn(term, fixture)
        for forbidden in ("#[tauri::command]", "open_database(", "AppHandle", "tauri::State"):
            self.assertNotIn(forbidden, fixture)
        self.assertIn("mod m32_v7_writer_service;",
                      (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8"))
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40647564175", body, filename)
            self.assertIn("M3_2_V7_RUST_SINGLE_OWNER_WRITER_PREPARATION_20261028.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40647564175", body, filename)
            self.assertIn("M3_2_V7_RUST_SINGLE_OWNER_WRITER_PREPARATION_20261028.md", body, filename)

    def test_136_pr204_terminal_and_new_writer_admission_continuity_strategy(self):
        terminal = self.data["post_pr204_terminal_observation"]
        self.assertEqual(terminal["pr"], 204)
        self.assertEqual(terminal["source_sha"], "edc69ff3b2f7b428658315882b1604001a19a0cc")
        self.assertEqual(terminal["source_ci"], {"run_id": 40651970744, "conclusion": "SUCCESS"})
        self.assertEqual(terminal["merge_sha"], "d2d8634a92d335d8e3810047a704ff44464135b1")
        self.assertEqual(terminal["postmain_ci"], {"run_id": 40653351119, "conclusion": "SUCCESS"})
        self.assertEqual(tuple(terminal[key] for key in ("rust_base_tests", "greenfield_runner_tests",
                                                    "sqlite_inventory_tests", "handoff_tests")),
                         (189, 7, 41, 135))
        self.assertEqual(terminal["issue38_terminal_comment"], 6463892458)
        self.assertTrue(terminal["protect_main_active_strict"])
        self.assertTrue(terminal["prepared_writer_source_qualified"])
        for key in ("runtime_admission_token_available", "tauri_state_registered", "writer_ipc_authorized"):
            self.assertFalse(terminal[key], key)
        self.assertEqual(terminal["operator_execution"], "NO_OPERATOR_EXECUTION")

        strategy = self.data["next_m32_v7_writer_admission_strategy_20261028"]
        self.assertEqual(strategy["base_main_sha"], terminal["merge_sha"])
        self.assertEqual(strategy["first_step"],
                         "S1_NEW_ONLY_VS_EXISTING_PROFILE_ADMISSION_CONTRACT_SOURCE_ONLY")
        self.assertEqual(strategy["same_profile"], "com.fabulaxiom.greenfield.v1")
        self.assertEqual(tuple(strategy[key] for key in ("rust_base_tests_expected",
            "greenfield_runner_tests_expected", "sqlite_inventory_tests_expected",
            "handoff_tests_expected")), (189, 7, 41, 136))
        self.assertTrue(strategy["prepared_writer_source_qualified"])
        for key in ("admission_runtime_implemented", "atomic_sqlite_pre_xopen_proven",
                    "writer_absence_proven", "writer_ipc_authorized", "operator_sqlite_access",
                    "migration_007_authorized", "native_hello_authorized", "strategy_document_ci_qualified"):
            self.assertFalse(strategy[key], key)
        self.assertEqual(strategy["operator_execution"], "NO_OPERATOR_EXECUTION")
        for key, value in (("m3_2", "IN_PROGRESS_NOT_ACCEPTED"), ("g2b", "NOT_ACCEPTED"),
                           ("writer", "NOT_PROVEN"), ("g2c", "NOT_AUTHORIZED"),
                           ("real_g3", "STOP_UNAVAILABLE"),
                           ("historical", "PENDING_EXTERNAL_ATTESTATION(21/3/2)"),
                           ("prospective", "NOT_STARTED")):
            self.assertEqual(strategy[key], value)

        doc = (ROOT / strategy["strategy"]).read_text(encoding="utf-8")
        for signal in ("PR #204", "40651970744", "40653351119", "6463892458",
                       "S0", "S1", "S2", "S3", "S4", "NEW_ONLY", "EXISTING_PROFILE",
                       "-wal", "-shm", "-journal", "TOCTOU", "189 Rust", "135 contrats",
                       "com.fabulaxiom.greenfield.v1", "NOT_PROVEN", "NOT_AUTHORIZED",
                       "STOP_UNAVAILABLE", "autorisation distincte", "aucun constructeur"):
            self.assertIn(signal, doc, signal)
        for filename in ("RESUME_PROMPT_SHORT.md", "RESUME_PROMPT.md", "HANDOFF_CURRENT.md",
                         "HANDOFF_PROTOCOL.md", "HANDOFF_HISTORY.md", "NEXT.md", "STATE.md",
                         "M3_2_GATE_DECISION_CURRENT.md", "README.md"):
            body = (DIRECTORY / filename).read_text(encoding="utf-8")
            self.assertIn("40653351119", body, filename)
            self.assertIn("M3_2_V7_WRITER_ADMISSION_STRATEGY_20261028.md", body, filename)
        for filename in ("ROADMAP_STATUS_CURRENT.md", "FABULAXIOM_ROADMAP_V1.md"):
            body = (ROOT / "docs/roadmap" / filename).read_text(encoding="utf-8")
            self.assertIn("40653351119", body, filename)
            self.assertIn("M3_2_V7_WRITER_ADMISSION_STRATEGY_20261028.md", body, filename)

    def test_137_s1_s2_preflight_has_no_runtime_token_or_operator_access(self):
        candidate = (ROOT / "src-tauri/src/m32_v7_admission_preflight_tests.rs").read_text(encoding="utf-8")
        backend = (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8")
        writer = (ROOT / "src-tauri/src/m32_v7_writer_service.rs").read_text(encoding="utf-8")
        scope = (ROOT / "docs/qualification/M3_2_V7_ADMISSION_S1_S2_DISPOSABLE_PREFLIGHT_20261028.md").read_text(encoding="utf-8")
        self.assertIn("#[cfg(all(test, windows))]", backend)
        self.assertIn("mod m32_v7_admission_preflight_tests;", backend)
        self.assertIn("Err(Refusal::HandoffNotAtomic)", candidate)
        self.assertIn("create_new(true)", candidate)
        self.assertIn("create_dir_all(self.db().parent()", candidate)
        for signal in ("NewOnly", "ExistingProfile", "-wal", "-shm", "-journal", "ForeignSchema", "ForeignKeyViolation"):
            self.assertIn(signal, candidate)
        self.assertNotIn("V7WriterAdmission {", candidate)
        self.assertIn("#[cfg(test)]\nimpl V7WriterAdmission", writer)
        for stop in ("NOT_PROVEN", "NOT_AUTHORIZED", "STOP_UNAVAILABLE", "S3/S4"):
            self.assertIn(stop, scope)

    def test_138_s2_namespace_concurrency_and_live_wal_remain_non_admission(self):
        fixture = (ROOT / "src-tauri/src/m32_v7_admission_preflight_tests.rs").read_text(encoding="utf-8")
        qualification = (ROOT / "docs/qualification/M3_2_V7_S2_NAMESPACE_CONCURRENCY_WAL_20261028.md").read_text(encoding="utf-8")
        for signal in ("m32_s2_two_simultaneous_new_only_claims", "m32_s2_parent_namespace_replacement",
                       "m32_s2_live_wal_and_external_connection_lock", "create_new(true)",
                       "BEGIN IMMEDIATE", "Err(Refusal::HandoffNotAtomic)"):
            self.assertIn(signal, fixture, signal)
        self.assertIn("#[cfg(all(test, windows))]", (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8"))
        self.assertNotIn("V7WriterAdmission {", fixture)
        for stop in ("NOT_PROVEN", "STOP_UNAVAILABLE", "S3/S4", "not atomic"):
            self.assertIn(stop, qualification)

    def test_139_s2_route_a_controlled_namespace_is_test_only_and_still_unbound(self):
        src = (ROOT / "src-tauri/src/m32_v7_admission_preflight_tests.rs").read_text(encoding="utf-8")
        lib = (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8")
        decision = (ROOT / "docs/qualification/M3_2_V7_S2_ROUTE_A_OWNED_NAMESPACE_BOUNDARY_20261028.md").read_text(encoding="utf-8")
        for signal in ("owned_namespace_preflight", "OutsideOwnedRoot", "UnsafeOwnedAncestor",
                       "FILE_ATTRIBUTE_REPARSE_POINT", "m32_s2_route_a_owned_namespace",
                       "m32_s2_route_a_parent_missing", "HandoffNotAtomic"):
            self.assertIn(signal, src, signal)
        self.assertIn("#[cfg(all(test, windows))]", lib)
        self.assertNotIn("V7WriterAdmission {", src)
        for signal in ("controlled namespace", "NOT_PROVEN", "S3/S4", "STOP_UNAVAILABLE",
                       "not atomic", "no operator"):
            self.assertIn(signal, decision)

    def test_140_s1_route_a_lifecycle_model_is_not_runtime_admission(self):
        src = (ROOT / "src-tauri/src/m32_v7_admission_preflight_tests.rs").read_text(encoding="utf-8")
        doc = (ROOT / "docs/qualification/M3_2_V7_S1_ROUTE_A_LIFECYCLE_DECISION_20261028.md").read_text(encoding="utf-8")
        for signal in ("LifecycleObservation", "UncertainAfterCrash", "CleanlyClosed",
                       "LifecycleUnproven", "m32_s1_route_a_clean_close",
                       "m32_s1_route_a_uncertain_or_foreign", "HandoffNotAtomic"):
            self.assertIn(signal, src)
        self.assertNotIn("V7WriterAdmission {", src)
        self.assertIn("#[cfg(all(test, windows))]", (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8"))
        for signal in ("NOT PASS", "NOT_PROVEN", "STOP_UNAVAILABLE", "S3/S4",
                       "no IPC", "no atomic", "not a trustworthy runtime evidence"):
            self.assertIn(signal, doc)

    def test_141_s1_route_a_explicit_close_observation_is_ephemeral(self):
        src = (ROOT / "src-tauri/src/m32_v7_admission_preflight_tests.rs").read_text(encoding="utf-8")
        doc = (ROOT / "docs/qualification/M3_2_V7_S1_ROUTE_A_INPROCESS_CLOSE_OBSERVATION_20261028.md").read_text(encoding="utf-8")
        for term in ("observe_disposable_explicit_close", "connection.close()",
                     "m32_s1_route_a_explicit_close_witness_is_inprocess_only",
                     "m32_s1_route_a_implicit_drop_cannot_mint_reopen_evidence",
                     "UncertainAfterCrash", "HandoffNotAtomic"):
            self.assertIn(term, src)
        self.assertNotIn("V7WriterAdmission {", src)
        self.assertIn("#[cfg(all(test, windows))]", (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8"))
        for term in ("NOT PASS", "NOT_PROVEN", "STOP_UNAVAILABLE", "S3/S4",
                     "not a crash test", "no durable record", "no atomic xOpen"):
            self.assertIn(term.lower(), doc.lower())

    def test_142_s1_cross_process_provenance_design_keeps_admission_stopped(self):
        doc = (ROOT / "docs/qualification/M3_2_V7_S1_ROUTE_A_CROSS_PROCESS_PROVENANCE_DESIGN_REVIEW_20261028.md").read_text(encoding="utf-8")
        for signal in ("A0", "A1", "A2", "A3", "UNAVAILABLE_NOT_PROVEN",
                       "EXISTING_PROFILE", "NEW_ONLY", "Handoff", "NOT_PROVEN",
                       "STOP_UNAVAILABLE", "S3/S4", "no code or operator action",
                       "authorization required", "no persistent marker"):
            self.assertIn(signal.lower(), doc.lower())
        self.assertIn("#[cfg(all(test, windows))]", (ROOT / "src-tauri/src/lib.rs").read_text(encoding="utf-8"))
        writer = (ROOT / "src-tauri/src/m32_v7_writer_service.rs").read_text(encoding="utf-8")
        self.assertIn("#[cfg(test)]\nimpl V7WriterAdmission", writer)

    def test_145_delegated_xopen_native_handle_veto_is_test_only(self):
        src = (ROOT / "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs").read_text(encoding="utf-8")
        doc = (ROOT / "docs/qualification/M3_2_V7_SQLITE_XOPEN_DELEGATED_HANDLE_BOUNDARY_DECISION_20261028.md").read_text(encoding="utf-8")
        for signal in ("check_delegated_handle", "xFileControl", "SQLITE_FCNTL_WIN32_GET_HANDLE",
                       "delegated_handle_refusals", "xClose", "SQLITE_CANTOPEN",
                       "m32_vfs_fixture_xopen_delegated_handle_matches",
                       "m32_vfs_fixture_xopen_delegated_substitution_closes_and_vetoes"):
            self.assertIn(signal, src)
        self.assertNotIn("V7WriterAdmission {", src)
        for signal in ("NOT PASS", "NOT_PROVEN", "STOP_UNAVAILABLE", "A0",
                       "S3/S4", "no operator", "xOpen", "not atomic", "no IPC"):
            self.assertIn(signal.lower(), doc.lower())

    def test_144_a2_a3_windows_disposable_proof_remains_a_veto(self):
        src = (ROOT / "src-tauri/src/m32_v7_admission_preflight_tests.rs").read_text(encoding="utf-8")
        doc = (ROOT / "docs/qualification/M3_2_V7_S1_S2_A2_A3_DISPOSABLE_EXPERIMENT_20261028.md").read_text(encoding="utf-8")
        for signal in ("CreateMutexW", "WaitForSingleObject", "WAIT_ABANDONED",
                       "m32_s2_a2_two_cooperating_processes", "m32_s2_a2_abandoned",
                       "a3_disposable_integrity_veto", "m32_s2_a3_corrupted",
                       "m32_s2_a3_wal_sidecar", "HandoffNotAtomic"):
            self.assertIn(signal, src)
        self.assertNotIn("V7WriterAdmission {", src)
        for signal in ("A0", "NOT_PROVEN", "STOP_UNAVAILABLE", "no atomic",
                       "S3/S4", "no operator", "security descriptor", "NOT PASS"):
            self.assertIn(signal.lower(), doc.lower())

    def test_143_s1_route_a_a2_a3_design_has_no_runtime_authority(self):
        doc = (ROOT / "docs/qualification/M3_2_V7_S1_ROUTE_A_A2_A3_COMBINED_DESIGN_20261028.md").read_text(encoding="utf-8")
        for signal in ("design study only", "named mutex", "COORDINATION_UNPROVEN",
                       "RECOVERY_REQUIRED_NOT_AUTHORIZED", "FOREIGN_PROVENANCE",
                       "INVALID_FIXTURE", "STRUCTURALLY_CONSISTENT_UNAUTHENTICATED",
                       "HandoffNotAtomic", "WAIT_ABANDONED", "NEW_ONLY", "EXISTING_PROFILE",
                       "A0", "NOT_PROVEN", "STOP_UNAVAILABLE", "S3/S4",
                       "no operator execution", "implementation gate"):
            self.assertIn(signal.lower(), doc.lower())
        rust = (ROOT / "src-tauri/src/m32_v7_writer_service.rs").read_text(encoding="utf-8")
        self.assertIn("#[cfg(test)]\nimpl V7WriterAdmission", rust)


    def test_146_d3c_r7_design_is_not_a_runtime_or_disposable_fixture_authorization(self):
        design_name = "M3_2_V7_P1_D3C_R7_RESTART_PROVENANCE_DESIGN_20261029.md"
        doc = (ROOT / "docs/qualification" / design_name).read_text(encoding="utf-8")
        short = (DIRECTORY / "RESUME_PROMPT_SHORT.md").read_text(encoding="utf-8")
        detailed = (DIRECTORY / "RESUME_PROMPT.md").read_text(encoding="utf-8")
        for needle in ("D3c", "DESIGN PROPOSAL", "NOT AUTHORIZED", "RECOVERY_REQUIRED_NOT_AUTHORIZED", "EXISTING_PROFILE", "R1–R9", "D3c-12", "no production", "not recovery"):
            self.assertIn(needle.lower(), doc.lower(), needle)
        self.assertIn("D3c", short)
        self.assertIn(design_name, detailed)
        self.assertIn(design_name, self.doc)
        self.assertIn(design_name, self.policy)
        checkpoint = self.data["d3c_r7_design_checkpoint_20261029"]
        self.assertEqual(checkpoint["authority"], "NOT_AUTHORIZED_FOR_D3C_CODE_OR_FIXTURES")
        self.assertEqual(checkpoint["a0_existing_profile"], "STOP")
        for key in ("d3c_test_implemented", "d3c_r7_production_proven",
                    "persistent_marker_authorized", "crash_recovery_authorized",
                    "writer_ipc_authorized", "migration_007_authorized"):
            self.assertFalse(checkpoint[key], key)
        self.assertIn("#[cfg(test)]\nimpl V7WriterAdmission",
                      (ROOT / "src-tauri/src/m32_v7_writer_service.rs").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
