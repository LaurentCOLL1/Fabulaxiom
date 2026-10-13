"""Stage-13 source anchor tests: all inputs are synthetic manifest fixtures."""
import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_independent_authority_gate as authority
from m3_2_operator_readonly_gate import GateStop


class Stage13PinnedSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="fabulaxiom-m32-stage13-synthetic-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.manifest = self.root / "manifest.json"
        records = []
        for root, role in sorted(authority.ALL_ROLES):
            key = (root, role)
            path = authority.EXACT_PATHS.get(key)
            if path is None:
                prefix = "operator-qualification/m2_3/fabulaxiom.operator-pre-m2-3-v4.fixture.sqlite3"
                path = prefix + (".manifest.json" if role == "pre_m23_manifest" else "")
            if key in authority.PINNED_SHA256:
                digest = authority.PINNED_SHA256[key]
                label = "historical"
            elif key in authority.OBSERVED_SHA256:
                digest = authority.OBSERVED_SHA256[key]
                label = "observed"
            else:
                digest = "a" * 64
                label = "observed"
            records.append({
                "root": root, "role": role,
                "path": path, "sha256": digest, "authority": label
            })
        self.records = records
        self.write()

    def write(self):
        obj = {
            "protocol": authority.stage12.PROTOCOL,
            "expected_head": "b" * 40,
            "expected_main": "c" * 40,
            "protected_files": self.records,
        }
        self.manifest.write_text(json.dumps(obj), encoding="utf-8")
        self.sha = hashlib.sha256(self.manifest.read_bytes()).hexdigest()

    def get(self, root, role):
        return next(item for item in self.records
                    if item["root"] == root and item["role"] == role)

    def test_exhaustive_pinned_scope_pending_correctly(self):
        summary = authority.validate_anchored_records(self.records)
        self.assertEqual(summary, {
            "source_pinned": len(authority.PINNED_SHA256),
            "recent_observation": len(authority.OBSERVED_SHA256),
            "unanchored": len(authority.UNANCHORED_OBSERVED),
        })
        self.assertEqual(sum(summary.values()), 26)

    def test_two_distinct_named_v5_backups_identical_sha_allowed(self):
        early = self.get("production", "pre_m24_early_v5")
        late = self.get("production", "pre_m24_v5")
        self.assertEqual(early["sha256"], late["sha256"])
        self.assertNotEqual(early["path"], late["path"])
        self.assertEqual(authority.validate_anchored_records(self.records)["source_pinned"],
                         len(authority.PINNED_SHA256))

    def test_observed_acl_promoted_to_historical_refused(self):
        for role in ("original_acls", "pre_repair_json"):
            candidate = copy.deepcopy(self.records)
            for e in candidate:
                if e["root"] == "acl" and e["role"] == role:
                    e["authority"] = "historical"
            with self.assertRaisesRegex(GateStop, "observed_not_independently_historical"):
                authority.validate_anchored_records(candidate)

    def test_early_manifest_recent_hash_cannot_be_promoted(self):
        self.get("production", "pre_m24_early_manifest")["authority"] = "historical"
        with self.assertRaisesRegex(GateStop, "observed_not_independently_historical"):
            authority.validate_anchored_records(self.records)

    def test_missing_independent_marker_source_remains_observed(self):
        self.get("production", "activation_marker")["authority"] = "historical"
        with self.assertRaisesRegex(GateStop, "unanchored_role_not_historical"):
            authority.validate_anchored_records(self.records)

    def test_wrong_source_pinned_sha_refused_even_when_self_manifest_matches(self):
        self.get("production", "pre_m24_v5")["sha256"] = "f" * 64
        self.write()
        with self.assertRaisesRegex(GateStop, "source_pinned_sha_or_label_mismatch"):
            authority.validate_anchored_records(self.records)

    def test_valid_hash_on_wrong_named_backup_rejected(self):
        early = self.get("production", "pre_m24_early_v5")
        early["path"] = authority.EXACT_PATHS[("production", "pre_m24_v5")]
        with self.assertRaisesRegex(GateStop, "exact_path_mismatch"):
            authority.validate_anchored_records(self.records)

    def test_pre_m23_backup_manifest_must_be_same_named_pair(self):
        self.get("production", "pre_m23_manifest")["path"] = (
            "operator-qualification/m2_3/fabulaxiom.operator-pre-m2-3-v4.other.sqlite3.manifest.json"
        )
        with self.assertRaisesRegex(GateStop, "pre_m23_pair_mismatch"):
            authority.validate_anchored_records(self.records)

    def test_bad_variable_path_prefix_traversal_refused(self):
        self.get("production", "pre_m23_v4")["path"] = (
            "operator-qualification/m2_3/../fabulaxiom.operator-pre-m2-3-v4.x.sqlite3"
        )
        with self.assertRaisesRegex(GateStop, "historical_directory_or_name_invalid"):
            authority.validate_anchored_records(self.records)

    def test_duplicate_missing_and_unapproved_roles_refused(self):
        with self.assertRaisesRegex(GateStop, "scope_incomplete"):
            authority.validate_anchored_records(self.records[:-1])
        items = copy.deepcopy(self.records)
        items[0] = copy.deepcopy(items[1])
        with self.assertRaisesRegex(GateStop, "unknown_or_duplicate"):
            authority.validate_anchored_records(items)
        items = copy.deepcopy(self.records)
        items[0]["role"] = "attacker_owned_file"
        with self.assertRaisesRegex(GateStop, "unknown_or_duplicate"):
            authority.validate_anchored_records(items)

    def test_manifest_untrusted_labels_gate_before_scope_reads(self):
        self.get("acl", "original_acls")["authority"] = "historical"
        self.write()
        with mock.patch.object(authority.stage12, "inspect",
                               side_effect=AssertionError("must not inspect other roots")):
            with self.assertRaisesRegex(GateStop, "observed_not_independently_historical"):
                self.check_inspect()

    def check_inspect(self, **extra):
        kw = dict(
            source_repo=self.source, expected_head="b"*40, expected_main="c"*40,
            production_root=self.root / "com.fabulaxiom.desktop",
            m25_root=self.root / "com.fabulaxiom.m25qual35fb842c",
            m31_root=self.root / ("com.fabulaxiom.m31launch" + "d"*32),
            acl_root=self.root / "Fabulaxiom-M31-ACL-Evidence-4d520e18",
            protected_manifest=self.manifest, expected_manifest_sha256=self.sha,
            proposed_identity="com.fabulaxiom.m32gate" + "e"*32,
            app_stopped=True, token_checker=lambda: True,
        )
        kw.update(extra)
        return authority.inspect(**kw)

    def test_manifest_digest_must_be_independently_supplied(self):
        with mock.patch.object(authority.stage12, "inspect",
                               side_effect=AssertionError("must fail before scope")):
            with self.assertRaisesRegex(GateStop, "manifest_sha_mismatch"):
                self.check_inspect(expected_manifest_sha256="e"*64)

    def test_pending_even_when_stage12_validates_bytes(self):
        before = self.manifest.read_bytes()
        with mock.patch.object(authority.stage12, "inspect", return_value={
            "status": "PENDING_HISTORICAL_AUTHORITY",
            "writes_performed": False,
            "m32_staging_authorized": False,
        }):
            result = self.check_inspect()
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertFalse(result["m32_staging_authorized"])
        self.assertFalse(result["operator_live_qualified"])
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_false_medium_token_prevents_scope_read(self):
        with mock.patch.object(authority.stage12, "_manifest_read",
                               side_effect=AssertionError("must not read")):
            with self.assertRaisesRegex(GateStop, "medium_token"):
                self.check_inspect(token_checker=lambda: False)


if __name__ == "__main__":
    unittest.main()
