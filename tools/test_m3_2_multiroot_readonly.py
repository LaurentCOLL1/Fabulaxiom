"""Disposable-only multi-root custody tests. Never touch operator files."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_multiroot_readonly as stage12

HEAD = "a" * 40
MAIN = "b" * 40
IDENTITY = "com.fabulaxiom.m32gate" + "c" * 32
M31_NAME = "com.fabulaxiom.m31launch" + "d" * 32
ACTIVE_NAME = "fabulaxiom-restored-" + "1" * 32 + "-" + "2" * 10 + "-" + "3" * 10 + ".sqlite3"
MARKER_NAME = "activation-" + "1" * 32 + "-" + "2" * 10 + "-" + "3" * 10 + ".active"


class MultiRootSyntheticTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory(prefix="fabulaxiom-stage12-synthetic-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        parent = self.base / "app-local-data"
        parent.mkdir()
        self.roots = {
            "production": parent / "com.fabulaxiom.desktop",
            "m25": parent / "com.fabulaxiom.m25qual35fb842c",
            "m31": parent / M31_NAME,
            "acl": self.base / "Fabulaxiom-M31-ACL-Evidence-4d520e18",
        }
        for folder in self.roots.values():
            folder.mkdir()
        self.manifest = self.base / "authority.json"
        self.entries = []
        for root_id, roles in stage12.ROLES.items():
            for role in sorted(roles):
                if role == "active_v6":
                    relative = "database/" + ACTIVE_NAME
                    payload = b"synthetic source active v6, no SQLite handle"
                elif role == "activation_marker":
                    relative = "database/activations/" + MARKER_NAME
                    payload = ACTIVE_NAME.encode("utf-8")
                elif role == "original_acls":
                    relative = "original-acls.txt"
                    payload = b"synthetic archived DACL; NEVER restore"
                elif role == "pre_repair_json":
                    relative = "pre-repair-evidence.json"
                    payload = json.dumps({
                        "identity": M31_NAME, "original_owner_sid": "S-1-5-32-544",
                        "original_sddl": "O:BAG:BAD:(A;;FA;;;BA)",
                    }).encode("utf-8")
                else:
                    suffix = ".sqlite3" if role in stage12.SQLITE_ROLES else ".json"
                    relative = "fixtures/" + role + suffix
                    payload = ("synthetic " + root_id + " " + role).encode()
                file = self.roots[root_id] / relative
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(payload)
                self.entries.append({
                    "root": root_id, "role": role, "path": relative,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "authority": "observed" if root_id == "acl" else "historical",
                })
        self.write_manifest()

    def write_manifest(self):
        data = {
            "protocol": stage12.PROTOCOL,
            "expected_head": HEAD,
            "expected_main": MAIN,
            "protected_files": self.entries,
        }
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        self.sha = stage12.prior.digest_file(self.manifest)

    def snapshot(self):
        return {
            str(path.relative_to(self.base)): stage12.prior.digest_file(path)
            for path in self.base.rglob("*") if path.is_file()
        }

    @staticmethod
    def fake_git(repo, *args):
        if args == ("rev-parse", "HEAD"):
            return HEAD
        if args == ("rev-parse", "refs/remotes/origin/main"):
            return MAIN
        if args == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        raise AssertionError("unexpected git command")

    def check(self, **changes):
        kw = dict(
            source_repo=self.repo,
            expected_head=HEAD,
            expected_main=MAIN,
            production_root=self.roots["production"],
            m25_root=self.roots["m25"],
            m31_root=self.roots["m31"],
            acl_root=self.roots["acl"],
            protected_manifest=self.manifest,
            expected_manifest_sha256=self.sha,
            proposed_identity=IDENTITY,
            app_stopped=True,
            token_checker=lambda: True,
        )
        kw.update(changes)
        with mock.patch.object(stage12.prior, "git_value", side_effect=self.fake_git):
            return stage12.inspect(**kw)

    def test_complete_custody_still_pending_for_observed_acl(self):
        before = self.snapshot()
        result = self.check()
        self.assertEqual(result["status"], "PENDING_HISTORICAL_AUTHORITY")
        self.assertEqual(result["file_count"], sum(map(len, stage12.ROLES.values())))
        self.assertEqual(result["root_count"], 4)
        self.assertEqual(result["authority_counts"]["observed"], 2)
        self.assertEqual(result["m32_staging_authorized"], False)
        self.assertEqual(result["sqlite_opened"], False)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.roots["production"].parent / IDENTITY).exists())

    def test_scope_success_is_not_staging_authorization(self):
        for entry in self.entries:
            entry["authority"] = "historical"
        self.write_manifest()
        r = self.check()
        self.assertEqual(r["status"], "VERIFIED_SCOPE_ONLY")
        self.assertFalse(r["writes_performed"])
        self.assertFalse(r["m32_staging_authorized"])

    def test_identical_backup_hash_distinct_exact_names_allowed(self):
        prod = [e for e in self.entries if e["root"] == "production"]
        first = next(e for e in prod if e["role"] == "pre_m24_v5")
        second = next(e for e in prod if e["role"] == "pre_m24_early_v5")
        source = self.roots["production"] / first["path"]
        target = self.roots["production"] / second["path"]
        target.write_bytes(source.read_bytes())
        second["sha256"] = first["sha256"]
        self.write_manifest()
        self.assertEqual(self.check()["file_count"], len(self.entries))

    def test_tampered_backup_refused_without_repair(self):
        role = next(e for e in self.entries if e["role"] == "pre_m24_v5")
        path = self.roots[role["root"]] / role["path"]
        path.write_bytes(b"corrupt synthetic payload")
        before = self.snapshot()
        with self.assertRaisesRegex(stage12.prior.GateStop, "digest_changed"):
            self.check()
        self.assertEqual(self.snapshot(), before)

    def test_missing_role_and_duplicate_role_refused(self):
        self.entries.pop()
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "file_set_incomplete"):
            self.check()
        self.entries.append(dict(self.entries[0]))
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "duplicate_role"):
            self.check()

    def test_wrong_root_and_traversal_refused(self):
        item = next(e for e in self.entries if e["role"] == "pre_m21_v3")
        item["root"] = "acl"
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "unapproved_role"):
            self.check()
        item["root"] = "production"
        item["path"] = "../outside.sqlite3"
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "relative_path_invalid"):
            self.check()

    def test_changed_marker_refused_despite_correct_hash(self):
        marker = next(e for e in self.entries if e["role"] == "activation_marker")
        path = self.roots["production"] / marker["path"]
        path.write_text("fabulaxiom.sqlite3", encoding="utf-8")
        marker["sha256"] = stage12.prior.digest_file(path)
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "activation_mismatch"):
            self.check()

    def test_sidecar_refused_without_deletion(self):
        role = next(e for e in self.entries if e["role"] == "isolated_v7")
        sidecar = Path(str(self.roots["m31"] / role["path"]) + "-wal")
        sidecar.write_bytes(b"unprotected synthetic WAL")
        before = self.snapshot()
        with self.assertRaisesRegex(stage12.prior.GateStop, "sqlite_sidecar_present"):
            self.check()
        self.assertEqual(self.snapshot(), before)

    def test_occupied_new_identity_fails_without_mutation(self):
        name = self.roots["production"].parent / IDENTITY
        name.mkdir()
        with self.assertRaisesRegex(stage12.prior.GateStop, "already_exists"):
            self.check()
        self.assertTrue(name.is_dir())

    def test_manifest_hash_tamper_and_unknown_authority_fail(self):
        with self.assertRaisesRegex(stage12.prior.GateStop, "manifest_sha_mismatch"):
            self.check(expected_manifest_sha256="e"*64)
        self.entries[0]["authority"] = "signed-by-guess"
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "authority_invalid"):
            self.check()

    def test_wrong_git_head_and_token_fail_before_files(self):
        with mock.patch.object(stage12.prior, "digest_file",
                               side_effect=AssertionError("must not read protected files")):
            with self.assertRaisesRegex(stage12.prior.GateStop, "standard_medium_token"):
                self.check(token_checker=lambda: False)
            with self.assertRaisesRegex(stage12.prior.GateStop, "head_not_exact"):
                self.check(expected_head="d"*40)

    def test_acl_identity_tamper_and_root_safety(self):
        item = next(e for e in self.entries if e["role"] == "pre_repair_json")
        path = self.roots["acl"] / item["path"]
        path.write_text(json.dumps({
            "identity": "com.fabulaxiom.desktop",
            "original_owner_sid": "S-1-5-32-544",
            "original_sddl": "sample"
        }), encoding="utf-8")
        item["sha256"] = stage12.prior.digest_file(path)
        self.write_manifest()
        with self.assertRaisesRegex(stage12.prior.GateStop, "acl_metadata_mismatch"):
            self.check()
        with self.assertRaisesRegex(stage12.prior.GateStop, "unapproved_custody_root_identity"):
            self.check(m31_root=self.base / "another")


if __name__ == "__main__":
    unittest.main()
