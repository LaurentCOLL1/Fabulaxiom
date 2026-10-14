"""M3.2 Stage 19: synthetic, disposable external provenance claim fixtures."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_provenance_triage as triage
from m3_2_operator_readonly_gate import GateStop


class SyntheticProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory(prefix="fabulaxiom-m32-provenance-synthetic-")
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.claims = []
        for root, role in sorted(triage.REMAINING):
            key = (root, role)
            self.claims.append({
                "root": root, "role": role,
                "observed_sha256": triage.source.OBSERVED_SHA256.get(key),
                "evidence_kind": "recent_observation"
                    if key in triage.source.OBSERVED_SHA256 else "none",
                "evidence_uri": None, "recorded_at": None,
                "custodian": None, "record_id": None,
            })

    def entry(self, root, role):
        return next(v for v in self.claims
                    if v["root"] == root and v["role"] == role)

    def add_unverified_external_lead(self, root="acl", role="original_acls"):
        item = self.entry(root, role)
        item.update({
            "evidence_kind": "prior_external_claim",
            "evidence_uri": "https://independent.example/evidence/abc123",
            "recorded_at": "2026-10-10T08:15:00+02:00",
            "custodian": "External archive custodian",
            "record_id": "record-001",
        })

    def test_five_roles_pending_without_promotions(self):
        result = triage.triage_claims(self.claims)
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertEqual(result["roles_checked"], 5)
        self.assertEqual(result["historically_pinned_roles_unchanged"], 21)
        self.assertEqual(result["observed_sha_roles_unchanged"], 3)
        self.assertEqual(result["unanchored_roles_unchanged"], 2)
        self.assertEqual(result["claims"], {
            "no_claim": 2, "recent_observation": 3,
            "unverified_prior_external_claim": 0,
        })
        self.assertEqual(result["historical_promotions"], 0)
        self.assertFalse(result["m32_staging_authorized"])
        self.assertFalse(result["writes_performed"])
        self.assertFalse(result["signatures_verified"])

    def test_claimed_prior_external_record_still_unverified(self):
        self.add_unverified_external_lead()
        self.add_unverified_external_lead(
            "production", "pre_m24_early_manifest"
        )
        result = triage.triage_claims(self.claims)
        self.assertEqual(result["claims"]["unverified_prior_external_claim"], 2)
        self.assertEqual(result["independently_verified_historical_claims"], 0)
        self.assertEqual(result["historical_promotions"], 0)
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")

    def test_recent_acl_hash_must_match_checked_in_observation(self):
        self.entry("acl", "original_acls")["observed_sha256"] = "f"*64
        with self.assertRaisesRegex(GateStop, "observed_sha_mismatch"):
            triage.triage_claims(self.claims)

    def test_unanchored_marker_cannot_self_pin_its_sha(self):
        self.entry("production", "activation_marker")["observed_sha256"] = "f"*64
        with self.assertRaisesRegex(GateStop, "unanchored_must_not_self_pin"):
            triage.triage_claims(self.claims)

    def test_external_claim_on_unanchored_record_still_pending(self):
        self.add_unverified_external_lead("m25", "isolated_v6")
        result = triage.triage_claims(self.claims)
        self.assertEqual(result["unanchored_roles_unchanged"], 2)
        self.assertEqual(result["claims"]["unverified_prior_external_claim"], 1)
        self.assertEqual(result["historical_promotions"], 0)

    def test_missing_or_duplicate_role_refused(self):
        with self.assertRaisesRegex(GateStop, "exact_five_roles"):
            triage.triage_claims(self.claims[:-1])
        dup = deepcopy(self.claims)
        dup[-1] = deepcopy(dup[0])
        with self.assertRaisesRegex(GateStop, "unknown_or_duplicate"):
            triage.triage_claims(dup)

    def test_extra_role_forgery_refused(self):
        self.claims[0]["role"] = "unapproved_artifact"
        with self.assertRaisesRegex(GateStop, "unknown_or_duplicate"):
            triage.triage_claims(self.claims)

    def test_unexpected_authority_override_field_refused(self):
        self.claims[0]["independent_verified"] = True
        with self.assertRaisesRegex(GateStop, "record_shape_invalid"):
            triage.triage_claims(self.claims)

    def test_untrusted_uri_credentials_or_http_refused(self):
        self.add_unverified_external_lead()
        item = self.entry("acl", "original_acls")
        for uri in (
            "http://independent.example/record",
            "https://person:secret@independent.example/record",
            "file:///C:/fake/attestation.json",
            "https://independent.example/a#fragment",
        ):
            item["evidence_uri"] = uri
            with self.assertRaisesRegex(GateStop, "metadata_invalid"):
                triage.triage_claims(self.claims)

    def test_untrusted_record_without_timezone_refused(self):
        self.add_unverified_external_lead()
        self.entry("acl", "original_acls")["recorded_at"] = (
            "2026-10-10T08:15:00"
        )
        with self.assertRaisesRegex(GateStop, "metadata_invalid"):
            triage.triage_claims(self.claims)

    def test_untrusted_record_without_custodian_refused(self):
        self.add_unverified_external_lead()
        self.entry("acl", "original_acls")["custodian"] = ""
        with self.assertRaisesRegex(GateStop, "metadata_invalid"):
            triage.triage_claims(self.claims)

    def test_recent_observation_cannot_smuggle_claimed_witness(self):
        self.entry("acl", "original_acls")["record_id"] = "fake"
        with self.assertRaisesRegex(GateStop, "observation_must_not_claim"):
            triage.triage_claims(self.claims)

    def test_none_cannot_smuggle_evidence_metadata(self):
        self.entry("m25", "isolated_v6")["record_id"] = "fake"
        with self.assertRaisesRegex(GateStop, "none_must_have_no_evidence"):
            triage.triage_claims(self.claims)

    def write_claims(self, data=None):
        path = self.folder / "synthetic_claims.json"
        path.write_text(json.dumps(
            self.claims if data is None else data
        ), encoding="utf-8")
        return path

    def test_loader_readonly_returns_exact_synthetic_records(self):
        path = self.write_claims()
        before = path.read_bytes()
        records = triage.read_claims_readonly(path)
        self.assertEqual(records, self.claims)
        self.assertEqual(path.read_bytes(), before)

    def test_duplicate_json_keys_rejected_even_if_second_overrides_first(self):
        path = self.folder / "duplicates.json"
        # A plain json.loads silently accepts the last duplicate.
        path.write_text(
            '[{"root":"acl","root":"production","role":"original_acls"}]',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(GateStop, "json_duplicate_key"):
            triage.read_claims_readonly(path)

    def test_duplicate_nested_json_keys_rejected(self):
        path = self.folder / "duplicates.json"
        path.write_text(
            '{"outer":{"record_id":"one","record_id":"two"}}',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(GateStop, "json_duplicate_key"):
            triage.read_claims_readonly(path)

    def test_nonfinite_json_number_rejected(self):
        path = self.folder / "nonfinite.json"
        path.write_text('{"unsafe":NaN}', encoding="utf-8")
        with self.assertRaisesRegex(GateStop, "json_nonfinite_number"):
            triage.read_claims_readonly(path)

    def test_invalid_utf8_refused(self):
        path = self.folder / "invalid-utf8.json"
        path.write_bytes(b'\xff\xfe{"x":2}')
        with self.assertRaisesRegex(GateStop, "invalid_utf8_json"):
            triage.read_claims_readonly(path)

    def test_relative_path_rejected(self):
        with self.assertRaisesRegex(GateStop, "absolute_path_required"):
            triage.read_claims_readonly(Path("unsafe_relative.json"))

    def test_temporary_provenance_prefix_is_not_worktree(self):
        # Fixture prefix itself historically collided with a blanket
        # 'fabulaxiom-m32-*' rule on the GitHub Windows runner.
        path = self.write_claims()
        self.assertEqual(triage.read_claims_readonly(path), self.claims)

    def test_worktree_sha_pattern_is_protected_but_fixture_prefix_is_not(self):
        self.assertIsNotNone(triage.PROTECTED_SOURCE_NAME.fullmatch(
            "fabulaxiom-m32-v7readonly-f89d31fb"
        ))
        self.assertIsNone(triage.PROTECTED_SOURCE_NAME.fullmatch(
            "fabulaxiom-m32-provenance-synthetic-a83ed1"
        ))

    def test_generic_fabulaxiom_component_not_a_protected_root(self):
        # GitHub Actions Windows checkout uses D:\\a\\Fabulaxiom\\Fabulaxiom.
        # A generic parent directory name is not itself a custody root.
        safe = self.folder / "Fabulaxiom"
        safe.mkdir()
        path = safe / "claims.json"
        path.write_text(json.dumps(self.claims), encoding="utf-8")
        self.assertEqual(triage.read_claims_readonly(path), self.claims)

    def test_main_operator_repo_refused_on_windows(self):
        if os.name != "nt":
            self.skipTest("operator Windows drive name semantics only")
        # A pure M:\\Fabulaxiom path is operator custody, not an arbitrary
        # D:\\a\\Fabulaxiom CI test directory.
        from unittest import mock as local_mock
        path = Path(r"M:\Fabulaxiom\claims.json")
        with local_mock.patch.object(triage, "regular_safe",
                                     side_effect=AssertionError("not reached")):
            with self.assertRaisesRegex(GateStop, "protected_location"):
                triage.read_claims_readonly(path)

    def test_protected_original_custody_directory_refused(self):
        root = self.folder / "com.fabulaxiom.desktop"
        root.mkdir()
        path = root / "operator-provided-claims.json"
        path.write_text(json.dumps(self.claims), encoding="utf-8")
        with self.assertRaisesRegex(GateStop, "protected_location"):
            triage.read_claims_readonly(path)

    def test_protected_acl_custody_directory_refused(self):
        root = self.folder / "Fabulaxiom-M31-ACL-Evidence-4d520e18"
        root.mkdir()
        path = root / "claims.json"
        path.write_text(json.dumps(self.claims), encoding="utf-8")
        with self.assertRaisesRegex(GateStop, "protected_location"):
            triage.read_claims_readonly(path)

    def test_protected_worktree_directory_refused(self):
        root = self.folder / "Fabulaxiom-M32-v7readonly-f89d31fb"
        root.mkdir()
        path = root / "claims.json"
        path.write_text(json.dumps(self.claims), encoding="utf-8")
        with self.assertRaisesRegex(GateStop, "protected_location"):
            triage.read_claims_readonly(path)

    def test_second_read_change_is_a_veto(self):
        path = self.write_claims()
        before = path.read_bytes()
        calls = [0]
        original = triage._read_once
        def unstable(selected):
            calls[0] += 1
            if calls[0] == 2:
                return b'[{"tampered": true}]'
            return original(selected)
        with mock.patch.object(triage, "_read_once", side_effect=unstable):
            with self.assertRaisesRegex(GateStop, "changed_during_read"):
                triage.read_claims_readonly(path)
        self.assertEqual(path.read_bytes(), before)

    def test_metadata_identity_change_is_a_veto(self):
        path = self.write_claims()
        original = triage._stat_identity
        calls = [0]
        def unstable(selected):
            calls[0] += 1
            stamp = original(selected)
            if calls[0] == 2:
                return (*stamp[:-1], stamp[-1] + 1)
            return stamp
        with mock.patch.object(triage, "_stat_identity", side_effect=unstable):
            with self.assertRaisesRegex(GateStop, "changed_during_read"):
                triage.read_claims_readonly(path)

    def test_symlink_input_refused_when_platform_permits_creation(self):
        original = self.write_claims()
        link = self.folder / "untrusted-link.json"
        try:
            link.symlink_to(original)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable in this test environment")
        with self.assertRaisesRegex(GateStop, "reparse_point"):
            triage.read_claims_readonly(link)
        self.assertEqual(original.read_bytes(), json.dumps(self.claims).encode())

    def test_reparse_guard_fail_closed_without_touching_claims(self):
        path = self.write_claims()
        before = path.read_bytes()
        with mock.patch.object(triage, "regular_safe",
                               side_effect=GateStop("synthetic_reparse_point")):
            with mock.patch.object(triage, "_read_once",
                                   side_effect=AssertionError("must not open")):
                with self.assertRaisesRegex(GateStop, "synthetic_reparse_point"):
                    triage.read_claims_readonly(path)
        self.assertEqual(path.read_bytes(), before)

    def test_valid_cli_returns_pending_and_exit_two_without_writes(self):
        path = self.folder / "synthetic_claims.json"
        path.write_text(json.dumps(self.claims), encoding="utf-8")
        before = path.read_bytes()
        out = io.StringIO()
        with redirect_stdout(out):
            code = triage.main(["--claims-json", str(path), "--dry-run"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.getvalue())["status"],
                         "PENDING_EXTERNAL_ATTESTATION")
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(sorted(p.name for p in self.folder.iterdir()),
                         ["synthetic_claims.json"])

    def test_invalid_cli_has_no_file_modification_or_auto_repair(self):
        path = self.folder / "synthetic_claims.json"
        path.write_text('{"not_a_list":true}', encoding="utf-8")
        before = path.read_bytes()
        out = io.StringIO()
        with redirect_stdout(out):
            code = triage.main(["--claims-json", str(path), "--dry-run"])
        report = json.loads(out.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["m32_staging_authorized"])
        self.assertEqual(path.read_bytes(), before)

    def test_oversized_input_refused_without_reading_source_data(self):
        path = self.folder / "oversized.json"
        path.write_bytes(b" " * 16385)
        out = io.StringIO()
        with redirect_stdout(out):
            code = triage.main(["--claims-json", str(path), "--dry-run"])
        self.assertEqual(code, 2)
        self.assertIn("provenance_claims_input_invalid", out.getvalue())


if __name__ == "__main__":
    unittest.main()
