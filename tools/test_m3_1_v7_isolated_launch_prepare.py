"""Isolated M3.1 Tauri identity staging; all files inside disposable fixture."""
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import unittest

import m3_1_v6_audit as audit
import m3_1_v7_isolated_launch_prepare as launch
import test_m3_1_v7_final_readonly as real


class IsolatedLaunchPreparationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = real.RealV7FinalReadOnlyTests(
            methodName="test_real_candidate_constraints_ram_only"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def stage(self, prepare=False, **updates):
        f = self.fixture
        args = dict(
            root=f.root,
            custody=f.safety["relative_custody_dir"],
            third=f.copy["relative_rehearsal_dir"],
            active=f.name,
            source_sha=f.sha,
            logical_sha=f.logical,
            backup_sha=f.safety["backup_sha256"],
            custody_manifest_sha=f.safety["manifest_sha256"],
            third_sha=f.copy["candidate_sha256"],
            third_manifest_sha=f.copy["manifest_sha256"],
            sql_file=real.CANDIDATE_SQL,
            sql_sha=f.sql_sha,
            prepare=prepare,
        )
        args.update(updates)
        return launch.perform(**args)

    def test_dry_run_has_no_new_identity_or_write(self):
        names = set(self.fixture.root.parent.iterdir())
        result = self.stage()
        self.assertEqual(result["status"], "READY")
        self.assertFalse(result["isolated_identity_created"])
        self.assertFalse(result["tauri_launched"])
        self.assertEqual(set(self.fixture.root.parent.iterdir()), names)

    def test_prepare_new_identity_copy_and_tauri_overlay(self):
        f = self.fixture
        protected_before = {
            "source": audit._file_sha256(f.file),
            "third": f.copy["candidate_sha256"],
        }
        result = self.stage(prepare=True)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mode"], "isolated_v7_launch_prepared_not_launched")
        self.assertRegex(
            result["identity"], r"^com\.fabulaxiom\.m31launch[0-9a-f]{32}$"
        )
        root = f.root.parent / result["identity"]
        self.assertNotEqual(root, f.root)
        db = root / "database" / "fabulaxiom.sqlite3"
        self.assertEqual(audit._file_sha256(db), protected_before["third"])
        overlay = json.loads((root / "tauri.m31.isolated.conf.json").read_text())
        self.assertEqual(overlay["identifier"], result["identity"])
        self.assertFalse(overlay["bundle"]["active"])
        self.assertIn("ISOLATED", overlay["app"]["windows"][0]["title"])
        manifest = json.loads((root / "preparation-manifest.json").read_text())
        self.assertEqual(manifest["copy_sha256"], protected_before["third"])
        self.assertFalse(manifest["tauri_launched"])
        self.assertFalse(manifest["production_migrated"])
        self.assertEqual(audit._file_sha256(f.file), protected_before["source"])
        third = f.root / f.copy["relative_rehearsal_dir"] / "candidate-v7.sqlite3"
        self.assertEqual(audit._file_sha256(third), protected_before["third"])

    def test_separate_prepares_never_reuse_an_identity(self):
        a = self.stage(prepare=True)
        b = self.stage(prepare=True)
        self.assertNotEqual(a["identity"], b["identity"])
        for result in (a, b):
            self.assertTrue((
                self.fixture.root.parent / result["identity"] /
                "database" / "fabulaxiom.sqlite3"
            ).is_file())

    def test_sha_tamper_rejected_before_identity_creation(self):
        old = set(self.fixture.root.parent.iterdir())
        with self.assertRaises(Exception):
            self.stage(prepare=True, third_sha="0"*64)
        self.assertEqual(set(self.fixture.root.parent.iterdir()), old)

    def test_unapproved_production_root_name_rejected(self):
        old = set(self.fixture.root.parent.iterdir())
        with self.assertRaises(Exception):
            self.stage(prepare=True, root=self.fixture.root.parent/"wrong-name")
        self.assertEqual(set(self.fixture.root.parent.iterdir()), old)


if __name__ == "__main__":
    unittest.main()
