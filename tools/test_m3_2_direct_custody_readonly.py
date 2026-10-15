"""M3.2 Stage 16: disposable 26-role, manifest-free custody tests only."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_direct_custody_readonly as direct


HEAD = "a" * 40
MAIN = "b" * 40
IDENTITY = "com.fabulaxiom.m32gate" + "c" * 32


class DirectSourceCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="fabulaxiom-stage16-synthetic-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        local = self.base / "app-local-data"
        local.mkdir()
        self.roots = {
            "production": local / "com.fabulaxiom.desktop",
            "m25": local / direct.M25_NAME,
            "m31": local / direct.M31_NAME,
            "acl": self.base / direct.ACL_NAME,
        }
        for root in self.roots.values():
            root.mkdir()
        self.paths = {}
        for key in sorted(direct.authority.ALL_ROLES):
            root, role = key
            if key in direct.authority.EXACT_PATHS:
                rel = direct.authority.EXACT_PATHS[key]
            elif role == "pre_m23_v4":
                rel = "operator-qualification/m2_3/fabulaxiom.operator-pre-m2-3-v4.fixture.sqlite3"
            elif role == "pre_m23_manifest":
                rel = ("operator-qualification/m2_3/"
                       "fabulaxiom.operator-pre-m2-3-v4.fixture.sqlite3.manifest.json")
            else:
                raise AssertionError("unclassified path")
            path = self.roots[root] / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if role == "activation_marker":
                contents = Path(direct.authority.EXACT_PATHS[
                    ("production", "active_v6")
                ]).name.encode()
            elif role == "pre_repair_json":
                contents = json.dumps({
                    "identity": direct.M31_NAME,
                    "original_owner_sid": "S-1-5-32-544",
                    "original_sddl": "synthetic SDDL not an actual ACL",
                }).encode()
            else:
                contents = f"SYNTHETIC role {root}/{role}".encode()
            path.write_bytes(contents)
            self.paths[key] = path

    def snapshot(self):
        return {
            str(p.relative_to(self.base)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in self.base.rglob("*") if p.is_file()
        }

    @staticmethod
    def git(repo, *cmd):
        if cmd == ("rev-parse", "HEAD"):
            return HEAD
        if cmd == ("rev-parse", "refs/remotes/origin/main"):
            return MAIN
        if cmd == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        raise AssertionError(cmd)

    def fake_hash(self, path):
        for key, present in self.paths.items():
            if present == path:
                if key in direct.authority.PINNED_SHA256:
                    return direct.authority.PINNED_SHA256[key]
                if key in direct.authority.OBSERVED_SHA256:
                    return direct.authority.OBSERVED_SHA256[key]
                return hashlib.sha256(path.read_bytes()).hexdigest()
        raise AssertionError("unexpected file lookup")

    def check(self, hash_fn=None, git_fn=None, **overrides):
        kw = dict(
            source_repo=self.repo, expected_head=HEAD, expected_main=MAIN,
            production_root=self.roots["production"],
            m25_root=self.roots["m25"], m31_root=self.roots["m31"],
            acl_root=self.roots["acl"], proposed_identity=IDENTITY,
            app_stopped=True, token_checker=lambda: True,
        )
        kw.update(overrides)
        with mock.patch.object(direct.common, "git_value",
                               side_effect=git_fn or self.git):
            with mock.patch.object(direct.common, "digest_file",
                                   side_effect=hash_fn or self.fake_hash):
                return direct.inspect(**kw)

    def test_all_26_roles_check_without_manifest_or_created_files(self):
        before = self.snapshot()
        result = self.check()
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertEqual(result["roots_inspected"], 4)
        self.assertEqual(result["roles_checked"], 26)
        self.assertEqual(result["authority_counts"], {
            "historical_pinned": 21,
            "recent_observation": 3,
            "unanchored_observation": 2,
        })
        self.assertFalse(result["m32_staging_authorized"])
        self.assertFalse(result["operator_live_qualified"])
        self.assertFalse(result["sqlite_opened"])
        self.assertFalse(result["writes_performed"])
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.roots["production"].parent / IDENTITY).exists())

    def test_same_digest_distinct_named_v5_backup_roles_allowed(self):
        x = self.paths[("production", "pre_m24_v5")]
        y = self.paths[("production", "pre_m24_early_v5")]
        self.assertNotEqual(x, y)
        self.assertEqual(self.fake_hash(x), self.fake_hash(y))
        self.assertEqual(self.check()["roles_checked"], 26)

    def test_production_marker_points_to_exact_restored_active_database(self):
        marker = self.paths[("production", "activation_marker")]
        marker.write_text("fabulaxiom.sqlite3", encoding="utf-8")
        with self.assertRaisesRegex(direct.GateStop, "active_selection"):
            self.check()

    def test_newer_activation_marker_causes_fail_closed(self):
        marker = self.paths[("production", "activation_marker")]
        newer = marker.with_name(
            "activation-" + "9"*32 + "-" + "9"*10 + "-" + "9"*10 + ".active"
        )
        newer.write_text("fabulaxiom.sqlite3", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(direct.GateStop, "unexpected_activation_marker_inventory"):
            self.check()
        self.assertEqual(self.snapshot(), before)

    def test_unexpected_active_suffix_and_extra_marker_refused(self):
        marker = self.paths[("production", "activation_marker")]
        extra = marker.with_name("manual-override.active")
        extra.write_text("synthetic attempted override", encoding="utf-8")
        with self.assertRaisesRegex(direct.GateStop, "unexpected_activation_marker_inventory"):
            self.check()

    def test_marker_inventory_cannot_change_after_initial_scan(self):
        original = direct.enforce_activation_inventory
        counter = [0]
        def late_marker(paths):
            counter[0] += 1
            if counter[0] == 2:
                marker = paths[("production", "activation_marker")]
                marker.with_name("activation-" + "8"*32 + "-" + "8"*10 + "-" + "8"*10 + ".active").write_text(
                    "synthetic new activation", encoding="utf-8"
                )
            return original(paths)
        with mock.patch.object(direct, "enforce_activation_inventory",
                               side_effect=late_marker):
            with self.assertRaisesRegex(direct.GateStop, "unexpected_activation_marker_inventory"):
                self.check()

    def test_exact_single_activation_marker_remains_accepted(self):
        self.assertEqual(self.check()["status"], "PENDING_EXTERNAL_ATTESTATION")

    def test_unknown_historical_digest_fails_even_with_no_operator_manifest(self):
        original = self.fake_hash
        bad = self.paths[("production", "m31_v6_backup")]
        with self.assertRaisesRegex(direct.GateStop, "historical_pin_mismatch"):
            self.check(hash_fn=lambda p: "f"*64 if p == bad else original(p))

    def test_observed_acl_digest_change_fails_without_historical_promotion(self):
        original = self.fake_hash
        evidence = self.paths[("acl", "original_acls")]
        with self.assertRaisesRegex(direct.GateStop, "recent_observation_mismatch"):
            self.check(hash_fn=lambda p: "e"*64 if p == evidence else original(p))

    def test_unanchored_isolated_v6_is_not_promoted_to_historical(self):
        item = self.paths[("m25", "isolated_v6")]
        item.write_bytes(b"new synthetic contents; no historical SHA available")
        result = self.check()
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertEqual(result["authority_counts"]["unanchored_observation"], 2)

    def test_during_hash_change_is_fail_closed(self):
        original = self.fake_hash
        target = self.paths[("production", "pre_m21_v3")]
        probes = [0]
        def unstable(p):
            if p == target:
                probes[0] += 1
                return original(p) if probes[0] == 1 else "f"*64
            return original(p)
        with self.assertRaisesRegex(direct.GateStop, "during_read_content_change"):
            self.check(hash_fn=unstable)

    def test_missing_v4_or_ambiguous_v4_source_fails(self):
        v4 = self.paths[("production", "pre_m23_v4")]
        v4.unlink()
        with self.assertRaisesRegex(direct.GateStop, "exact_v4_name_not_unique"):
            self.check()
        v4.write_bytes(b"synthetic again")
        sibling = v4.with_name("fabulaxiom.operator-pre-m2-3-v4.another.sqlite3")
        sibling.write_bytes(b"another synthetic")
        with self.assertRaisesRegex(direct.GateStop, "exact_v4_name_not_unique"):
            self.check()

    def test_protected_sidecar_refused_and_never_cleaned_up(self):
        original = self.paths[("m31", "isolated_v7")]
        sidecar = Path(str(original) + "-wal")
        sidecar.write_bytes(b"unprotected synthetic WAL")
        before = self.snapshot()
        with self.assertRaisesRegex(direct.GateStop, "sqlite_sidecar_present"):
            self.check()
        self.assertEqual(self.snapshot(), before)

    def test_acl_archived_json_must_match_original_identity(self):
        path = self.paths[("acl", "pre_repair_json")]
        path.write_text(json.dumps({
            "identity": "com.fabulaxiom.desktop",
            "original_owner_sid": "S-1-5-32-544",
            "original_sddl": "fake",
        }), encoding="utf-8")
        with self.assertRaisesRegex(direct.GateStop, "acl_archive_metadata_mismatch"):
            self.check()

    def test_invalid_token_refuses_before_filesystem_probe(self):
        with mock.patch.object(direct.common, "regular_safe",
                               side_effect=AssertionError("should not access any file")):
            with self.assertRaisesRegex(direct.GateStop, "standard_medium_token"):
                self.check(token_checker=lambda: False)

    def test_wrong_git_head_or_main_refuses_before_protected_scan(self):
        with self.assertRaisesRegex(direct.GateStop, "source_head_mismatch"):
            self.check(expected_head="d"*40)
        with self.assertRaisesRegex(direct.GateStop, "origin_main_stale"):
            self.check(expected_main="d"*40)

    def test_no_app_stopped_ack_refused(self):
        with self.assertRaisesRegex(direct.GateStop, "app_stopped_ack"):
            self.check(app_stopped=False)

    def test_reused_proposed_identity_refused(self):
        target = self.roots["production"].parent / IDENTITY
        target.mkdir()
        with self.assertRaisesRegex(direct.GateStop, "identity_occupied"):
            self.check()
        self.assertTrue(target.is_dir())

    def test_wrong_isolated_m31_root_refused(self):
        with self.assertRaisesRegex(direct.GateStop, "root_identity_invalid"):
            self.check(m31_root=self.roots["production"])

    def test_missing_source_anchor_role_refused(self):
        missing = self.paths[("production", "pre_m24_v5")]
        missing.unlink()
        with self.assertRaisesRegex(direct.GateStop, "required_path_missing_or_unreadable"):
            self.check()

    def test_path_redirect_refusal_is_fail_closed(self):
        target = self.paths[("production", "app_backup_a")]
        regular = direct.common.regular_safe
        def guard(path, directory):
            if path == target:
                raise direct.GateStop("reparse_point_in_protected_path")
            return regular(path, directory)
        with mock.patch.object(direct.common, "regular_safe", side_effect=guard):
            with self.assertRaisesRegex(direct.GateStop, "reparse_point"):
                self.check()

    def run_with_real_file_hashes_and_disposable_pins(self):
        """Exercise actual hash reader, never spoof on-disk bytes in this test."""
        pinned = {
            key: hashlib.sha256(self.paths[key].read_bytes()).hexdigest()
            for key in direct.authority.PINNED_SHA256
        }
        observed = {
            key: hashlib.sha256(self.paths[key].read_bytes()).hexdigest()
            for key in direct.authority.OBSERVED_SHA256
        }
        with mock.patch.dict(direct.authority.PINNED_SHA256, pinned, clear=True):
            with mock.patch.dict(direct.authority.OBSERVED_SHA256, observed, clear=True):
                with mock.patch.object(direct.common, "git_value", side_effect=self.git):
                    return direct.inspect(
                        self.repo, HEAD, MAIN,
                        self.roots["production"], self.roots["m25"],
                        self.roots["m31"], self.roots["acl"],
                        IDENTITY, True, token_checker=lambda: True,
                    )

    def test_real_digest_full_scope_on_disposable_files(self):
        before = self.snapshot()
        result = self.run_with_real_file_hashes_and_disposable_pins()
        self.assertEqual(result["roles_checked"], 26)
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertFalse(result["m32_staging_authorized"])
        self.assertEqual(self.snapshot(), before)

    def test_real_digest_refuses_extra_marker(self):
        marker = self.paths[("production", "activation_marker")]
        marker.with_name("activation-" + "7"*32 + "-" + "7"*10 + "-" + "7"*10 + ".active").write_bytes(
            b"new synthetic marker"
        )
        with self.assertRaisesRegex(direct.GateStop, "unexpected_activation_marker_inventory"):
            self.run_with_real_file_hashes_and_disposable_pins()

    def test_real_sha256_helper_on_disposable_bytes(self):
        file = self.paths[("production", "active_v6")]
        self.assertEqual(direct.common.digest_file(file),
                         hashlib.sha256(file.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
