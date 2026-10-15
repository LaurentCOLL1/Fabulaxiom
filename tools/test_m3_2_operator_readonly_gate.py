"""Synthetic-only stage-11 post-restart gate tests; no operator files."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_operator_readonly_gate as gate


HEAD = "a" * 40
MAIN = "b" * 40
IDENTITY = "com.fabulaxiom.m32gate" + "c" * 32


class Stage11ReadOnlyGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory(prefix="fabulaxiom-m32-gate-synthetic-")
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.repo = base / "source"
        self.repo.mkdir()
        self.parent = base / "app-data"
        self.parent.mkdir()
        self.production = self.parent / "com.fabulaxiom.desktop"
        self.production.mkdir()
        (self.production / "database").mkdir()
        self.db = self.production / "database" / "fabulaxiom.sqlite3"
        self.db.write_bytes(b"synthetic, never a user database")
        self.pointer = self.production / "activation-marker.json"
        self.pointer.write_text('{"fixture":true}', encoding="utf-8")
        self.manifest = base / "expected-sha256.json"
        self.write_manifest()
        self.before = self.inventory()

    def write_manifest(self, contents=None):
        items = contents
        if items is None:
            items = [
                {"path": "database/fabulaxiom.sqlite3",
                 "sha256": hashlib.sha256(self.db.read_bytes()).hexdigest()},
                {"path": "activation-marker.json",
                 "sha256": hashlib.sha256(self.pointer.read_bytes()).hexdigest()},
            ]
        self.manifest.write_text(json.dumps({
            "protocol": "fabulaxiom_m32_protected_sha_manifest_v1",
            "protected_files": items,
        }), encoding="utf-8")

    def inventory(self):
        return {
            str(p.relative_to(self.parent)): (
                p.stat().st_size,
                hashlib.sha256(p.read_bytes()).hexdigest(),
            )
            for p in self.parent.rglob("*") if p.is_file()
        }

    @staticmethod
    def fake_git(repo, *args):
        if args == ("rev-parse", "HEAD"):
            return HEAD
        if args == ("rev-parse", "refs/remotes/origin/main"):
            return MAIN
        if args == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        raise AssertionError(f"unexpected git command {args}")

    def check(self, **changes):
        arguments = dict(
            source_repo=self.repo, expected_head=HEAD, expected_main=MAIN,
            production_root=self.production, protected_manifest=self.manifest,
            proposed_identity=IDENTITY, app_stopped=True,
            token_checker=lambda: True,
        )
        arguments.update(changes)
        with mock.patch.object(gate, "git_value", side_effect=self.fake_git):
            return gate.inspect(**arguments)

    def test_clean_readonly_ready_with_no_new_identity_or_files(self):
        self.assertEqual(self.check()["status"], "READY")
        self.assertEqual(self.check()["protected_files_verified"], 2)
        self.assertEqual(self.inventory(), self.before)
        self.assertFalse((self.parent / IDENTITY).exists())
        self.assertEqual(self.check()["writes_performed"], False)

    def test_unapproved_effective_token_refused_before_protected_inspection(self):
        with mock.patch.object(gate, "regular_safe",
                               side_effect=AssertionError("must not inspect")):
            with self.assertRaisesRegex(gate.GateStop, "standard_medium_token"):
                self.check(token_checker=lambda: False)
        self.assertEqual(self.inventory(), self.before)

    def test_missing_operator_ack_and_production_identity_refused(self):
        with self.assertRaisesRegex(gate.GateStop, "app_stopped_ack"):
            self.check(app_stopped=False)
        with self.assertRaisesRegex(gate.GateStop, "unapproved_m32_identity"):
            self.check(proposed_identity="com.fabulaxiom.desktop")
        self.assertEqual(self.inventory(), self.before)

    def test_sha_tamper_refused_without_repair(self):
        self.db.write_bytes(b"changed synthetic fixture")
        after_tamper = self.inventory()
        with self.assertRaisesRegex(gate.GateStop, "digest_changed"):
            self.check()
        self.assertEqual(self.inventory(), after_tamper)

    def test_preexisting_identity_refused_without_deletion(self):
        target = self.parent / IDENTITY
        target.mkdir()
        with self.assertRaisesRegex(gate.GateStop, "already_exists"):
            self.check()
        self.assertTrue(target.is_dir())
        self.assertEqual(self.inventory(), self.before)

    def test_dirty_git_refuses_before_data_inspection(self):
        with mock.patch.object(gate, "git_value", side_effect=lambda repo,*args:
            "changed" if args[0] == "status" else self.fake_git(repo,*args)):
            with mock.patch.object(gate, "digest_file",
                                   side_effect=AssertionError("must not hash")):
                with self.assertRaisesRegex(gate.GateStop, "not_clean"):
                    gate.inspect(self.repo, HEAD, MAIN, self.production,
                                 self.manifest, IDENTITY, True,
                                 token_checker=lambda: True)
        self.assertEqual(self.inventory(), self.before)

    def test_traversal_duplicate_and_invalid_manifest_fail_closed(self):
        for path in ("../activation-marker.json",
                     "/Windows/System32/config/SAM",
                     "database\\fabulaxiom.sqlite3"):
            self.write_manifest([
                {"path": path, "sha256": "a"*64},
                {"path": "activation-marker.json",
                 "sha256": hashlib.sha256(self.pointer.read_bytes()).hexdigest()},
            ])
            with self.assertRaisesRegex(gate.GateStop, "relative_path_invalid"):
                self.check()
            self.assertEqual(self.inventory(), self.before)
        valid = {"path": "database/fabulaxiom.sqlite3",
                 "sha256": hashlib.sha256(self.db.read_bytes()).hexdigest()}
        self.write_manifest([valid, valid])
        with self.assertRaisesRegex(gate.GateStop, "duplicate"):
            self.check()

    def test_wrong_git_head_or_main_refuses(self):
        with self.assertRaisesRegex(gate.GateStop, "head_not_exact"):
            self.check(expected_head="d"*40)
        with self.assertRaisesRegex(gate.GateStop, "main_not_exact"):
            self.check(expected_main="d"*40)
        self.assertEqual(self.inventory(), self.before)


if __name__ == "__main__":
    unittest.main()
