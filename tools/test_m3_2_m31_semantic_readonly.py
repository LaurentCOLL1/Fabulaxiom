"""Stage 14: semantic archive tests on synthetic dicts and disposable files only."""
import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_m31_semantic_readonly as semantic
from m3_2_operator_readonly_gate import GateStop


class M31SemanticArchiveTests(unittest.TestCase):
    def setUp(self):
        self.docs = self.valid_documents()

    @staticmethod
    def valid_documents():
        l = semantic.LOGICAL_V6
        backup_item = lambda filename: {
            "file": filename, "sha256": semantic.V6,
            "combined_logical_sha256": l,
            "legacy_table_counts": {"table_" + str(i): i for i in range(14)},
            "integrity": "ok", "foreign_key_check": "ok",
        }
        return {
            "backup": {
                "protocol": "m3_1_operator_pre_v7_v6_backup_and_restore_v1",
                "source": {
                    "active_file": Path(semantic.pinned.EXACT_PATHS[
                        ("production", "active_v6")]).name,
                    "sha256": semantic.SOURCE, "logical_sha256": l,
                    "logical_algorithm": "fabulaxiom-v6-typed-row-sha256-v1",
                    "schema_version": 6,
                },
                "backup": backup_item("fabulaxiom-pre-m3-1-v6.sqlite3"),
                "restore_rehearsal": backup_item("isolated-restore-rehearsal-v6.sqlite3"),
                "active_pointer_modified": False,
                "migration_v7_executed": False,
            },
            "third": {
                "protocol": "m3_1_copy_only_v7_rehearsal_v1",
                "candidate_sql_sha256": semantic.SQL007,
                "source_production_sha256": semantic.SOURCE,
                "source_v6_backup_sha256": semantic.V6,
                "source_custody_manifest_sha256": semantic.V6_MANIFEST,
                "baseline_legacy_logical_sha256": l,
                "copy_file": "candidate-v7.sqlite3",
                "copy": {
                    "schema_version": 7, "file_sha256": semantic.V7,
                    "legacy_data_preserved": True, "new_tables_strict": 3,
                    "new_tables_empty": 3, "integrity": "ok",
                    "foreign_keys": "ok",
                },
                "v7_applied_to_disposable_copy_only": True,
                "production_schema_version": 6,
                "production_migrated": False,
                "active_pointer_modified": False,
            },
            "rollback": {
                "protocol": "m3_1_fourth_copy_forced_rollback_v1",
                "original_production_schema_version": 6,
                "original_source_sha256": semantic.SOURCE,
                "original_v6_backup_sha256": semantic.V6,
                "original_v6_manifest_sha256": semantic.V6_MANIFEST,
                "candidate_sql_sha256": semantic.SQL007,
                "forced_sqlite_error": "SQLITE_CONSTRAINT_PRIMARYKEY",
                "rolled_back_file": "failed-v7-rolled-back-v6.sqlite3",
                "rolled_back_file_sha256": semantic.V6,
                "rolled_back_file_bytes": 200000,
                "rolled_back_schema_version": 6,
                "legacy_logical_sha256": l,
                "all_14_legacy_tables_preserved": True,
                "schema_inventory_identical_to_pre_failure": True,
                "fourth_copy_bytes_identical_to_pre_failure": True,
                "production_migrated": False, "active_pointer_modified": False,
            },
            "preparation": {
                "protocol": "m3_1_isolated_v7_launch_preparation_v1",
                "identity": semantic.M31_ID,
                "expected_launch_behavior": "normal_v6_runtime_refuses_v7",
                "source_production_schema_version": 6,
                "copy_schema_version": 7,
                "copy_file": "database/fabulaxiom.sqlite3",
                "copy_sha256": semantic.V7,
                "original_third_copy_sha256": semantic.V7,
                "candidate_sql_sha256": semantic.SQL007,
                "tauri_overlay_file": "tauri.m31.isolated.conf.json",
                "tauri_overlay_sha256": semantic.pinned.PINNED_SHA256[("m31", "overlay")],
                "tauri_launched": False, "production_migrated": False,
                "active_pointer_modified": False,
            },
            "overlay": {
                "productName": "Fabulaxiom M3.1 Isolated",
                "identifier": semantic.M31_ID,
                "bundle": {"active": False},
                "app": {"windows": [{"label": "main",
                                    "title": "Fabulaxiom M3.1 - ISOLATED v7 refusal check"}]},
            },
        }

    def check_rejected(self, fragment):
        with self.assertRaisesRegex(GateStop, fragment):
            semantic.validate_documents(self.docs, semantic.M31_ID)

    def test_complete_source_attested_chain_is_semantically_consistent(self):
        original = copy.deepcopy(self.docs)
        result = semantic.validate_documents(self.docs, semantic.M31_ID)
        self.assertEqual(result["semantic_m31_manifests_verified"], 4)
        self.assertTrue(result["semantic_m31_config_verified"])
        self.assertFalse(result["production_migration_authorized"])
        self.assertFalse(result["sqlite_integrity_retested"])
        self.assertEqual(original, self.docs)

    def test_wrong_m31_identity_refused(self):
        self.check_rejected_with_identity("com.fabulaxiom.m31launch" + "a"*32)

    def check_rejected_with_identity(self, identity):
        with self.assertRaisesRegex(GateStop, "isolated_identity"):
            semantic.validate_documents(self.docs, identity)

    def test_bad_backup_source_or_changed_active_file(self):
        self.docs["backup"]["source"]["sha256"] = "a"*64
        self.check_rejected("invalid_sha256")
        self.docs["backup"]["source"]["sha256"] = semantic.SOURCE
        self.docs["backup"]["source"]["active_file"] = "fabulaxiom.sqlite3"
        self.check_rejected("invalid_active_file")

    def test_backup_restore_mismatch_or_wrong_logical_digest(self):
        self.docs["backup"]["restore_rehearsal"]["sha256"] = "e"*64
        self.check_rejected("invalid_sha256")
        self.docs["backup"]["restore_rehearsal"]["sha256"] = semantic.V6
        self.docs["backup"]["backup"]["combined_logical_sha256"] = "e"*64
        self.check_rejected("invalid_combined_logical_sha256")

    def test_backup_fourteen_tables_typed_nonnegative(self):
        self.docs["backup"]["backup"]["legacy_table_counts"]["table_0"] = -1
        self.check_rejected("backup_table_values")
        self.docs["backup"]["backup"]["legacy_table_counts"]["table_0"] = 0
        self.docs["backup"]["backup"]["legacy_table_counts"].pop("table_13")
        self.check_rejected("backup_table_count")

    def test_v6_flags_must_be_boolean_false_not_zero_or_true(self):
        self.docs["backup"]["migration_v7_executed"] = 0
        self.check_rejected("invalid_migration_v7_executed")
        self.docs["backup"]["migration_v7_executed"] = True
        self.check_rejected("invalid_migration_v7_executed")

    def test_third_copy_wrong_sealed_backup_manifest_anchor(self):
        self.docs["third"]["source_custody_manifest_sha256"] = "f"*64
        self.check_rejected("invalid_source_custody_manifest_sha256")

    def test_third_copy_requires_empty_strict_v7_and_no_production_migration(self):
        self.docs["third"]["copy"]["new_tables_empty"] = 2
        self.check_rejected("invalid_new_tables_empty")
        self.docs["third"]["copy"]["new_tables_empty"] = 3
        self.docs["third"]["production_migrated"] = True
        self.check_rejected("invalid_production_migrated")

    def test_rollback_must_be_precise_error_and_exact_v6_bytes(self):
        self.docs["rollback"]["forced_sqlite_error"] = "SQLITE_BUSY"
        self.check_rejected("invalid_forced_sqlite_error")
        self.docs["rollback"]["forced_sqlite_error"] = "SQLITE_CONSTRAINT_PRIMARYKEY"
        self.docs["rollback"]["rolled_back_file_sha256"] = "a"*64
        self.check_rejected("invalid_rolled_back_file_sha256")

    def test_rollback_boolean_history_and_bytes_checks(self):
        self.docs["rollback"]["fourth_copy_bytes_identical_to_pre_failure"] = False
        self.check_rejected("invalid_fourth_copy_bytes_identical_to_pre_failure")
        self.docs["rollback"]["fourth_copy_bytes_identical_to_pre_failure"] = True
        self.docs["rollback"]["rolled_back_file_bytes"] = 0
        self.check_rejected("rollback_bytes")

    def test_preparation_identity_overlay_and_no_tauri_launch(self):
        self.docs["preparation"]["identity"] = "com.fabulaxiom.desktop"
        self.check_rejected("invalid_identity")
        self.docs["preparation"]["identity"] = semantic.M31_ID
        self.docs["preparation"]["tauri_launched"] = True
        self.check_rejected("invalid_tauri_launched")

    def test_overlay_not_an_active_production_bundle(self):
        self.docs["overlay"]["bundle"]["active"] = True
        self.check_rejected("invalid_active")
        self.docs["overlay"]["bundle"]["active"] = False
        self.docs["overlay"]["identifier"] = "com.fabulaxiom.desktop"
        self.check_rejected("invalid_identifier")

    def test_missing_manifest_or_bad_json_object(self):
        self.docs.pop("rollback")
        self.check_rejected("document_set")
        self.docs["rollback"] = []
        self.check_rejected("nonobject_document")

    def test_read_anchored_file_rejects_different_bytes_before_parse(self):
        with TemporaryDirectory(prefix="fabulaxiom-stage14-synthetic-") as temp:
            root = Path(temp)
            role = ("m31", "overlay")
            path = root / semantic.pinned.EXACT_PATHS[role]
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(GateStop, "digest_before_changed"):
                semantic.read_anchored_document(root, role)
            self.assertEqual(path.read_text(encoding="utf-8"), "{}")

    def test_parent_gate_pending_is_required_before_archival_read(self):
        with mock.patch.object(semantic.pinned, "inspect",
                               return_value={"status": "FAIL"}):
            with mock.patch.object(semantic, "read_anchored_document",
                                   side_effect=AssertionError("must not read")):
                with self.assertRaisesRegex(GateStop, "prior_authority_gate"):
                    self.fake_inspect()

    def test_semantics_stay_pending_even_when_every_document_is_valid(self):
        with mock.patch.object(semantic.pinned, "inspect", return_value={
            "status": "PENDING_EXTERNAL_ATTESTATION",
            "source_head": "f"*40, "writes_performed": False
        }):
            with mock.patch.object(semantic, "read_anchored_document",
                                   side_effect=lambda r,k: self.docs[
                                       next(label for label, pair
                                            in semantic.EXPECTED_FILES.items()
                                            if pair == k)]):
                result = self.fake_inspect()
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertFalse(result["m32_staging_authorized"])
        self.assertFalse(result["operator_live_qualified"])
        self.assertFalse(result["sqlite_opened"])

    def fake_inspect(self):
        root = Path("C:/synthetic")
        return semantic.inspect(
            root, "f"*40, "e"*40, root/"com.fabulaxiom.desktop",
            root/"com.fabulaxiom.m25qual35fb842c",
            root/semantic.M31_ID, root/"synthetic-acl",
            root/"manifest.json", "c"*64,
            "com.fabulaxiom.m32gate"+"a"*32,
            True, token_checker=lambda: True
        )


if __name__ == "__main__":
    unittest.main()
