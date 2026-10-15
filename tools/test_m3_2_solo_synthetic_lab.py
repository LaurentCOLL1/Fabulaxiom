"""Adversarial tests for disposable synthesized data ONLY."""
from __future__ import annotations

import hashlib
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

from m3_2_solo_synthetic_lab import (
    GateBlocked, backup_synthetic, independent_count_oracle, logical_digest,
    new_reserved_file, new_synthetic_source, restore_synthetic, selftest,
    sha256, validate_new_copy,
)


class SoloLabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="fabulaxiom-m32-test-")
        self.root = Path(self.tmp.name)
        for d in ("source", "backup", "restore"):
            (self.root / d).mkdir(mode=0o700)
        self.source = new_synthetic_source(self.root / "source", version=6)

    def tearDown(self):
        self.tmp.cleanup()

    def fresh(self):
        return backup_synthetic(self.source, self.root / "backup")

    def test_selftest_v6_v7_isolated(self):
        selftest()

    def test_fixture_integrity_and_history(self):
        sha = sha256(self.source)
        snapshot, manifest = self.fresh()
        self.assertEqual(sha, sha256(self.source))
        self.assertEqual(manifest["schema"], 6)
        self.assertEqual(manifest["counts"]["scene_text_revisions"], 2)
        self.assertNotEqual(snapshot, self.source)

    def test_copy_and_restore_verification(self):
        snapshot, manifest = self.fresh()
        restored, evidence = restore_synthetic(snapshot, self.root / "restore", manifest)
        self.assertEqual(evidence["digest"], manifest["digest"])
        self.assertNotEqual(restored, snapshot)
        self.assertNotEqual(restored, self.source)

    def test_rollback_collision_no_overwrite(self):
        output = self.root / "backup" / "snapshot.sqlite"
        output.write_bytes(b"preexisting protected sentinel")
        digest = sha256(output)
        with self.assertRaises(GateBlocked):
            self.fresh()
        self.assertEqual(digest, sha256(output))

    def test_restore_collision_no_overwrite(self):
        snapshot, manifest = self.fresh()
        output = self.root / "restore" / "restore.sqlite"
        output.write_bytes(b"occupied")
        digest = sha256(output)
        with self.assertRaises(GateBlocked):
            restore_synthetic(snapshot, self.root / "restore", manifest)
        self.assertEqual(digest, sha256(output))

    def test_wrong_hash_rejected(self):
        path, manifest = self.fresh()
        with self.assertRaisesRegex(GateBlocked, "SHA-256"):
            validate_new_copy(path, schema=6, expected_sha256="0" * 64)

    def test_wrong_logical_digest_rejected(self):
        path, manifest = self.fresh()
        with self.assertRaisesRegex(GateBlocked, "logical digest"):
            validate_new_copy(path, schema=6, expected_digest="0" * 64)

    def test_wrong_version_rejected(self):
        path, manifest = self.fresh()
        with self.assertRaisesRegex(GateBlocked, "schema version"):
            validate_new_copy(path, schema=7)

    def test_missing_revision_rejected(self):
        path, manifest = self.fresh()
        with closing(sqlite3.connect(path)) as conn, conn:
            conn.execute("DELETE FROM scene_text_revisions WHERE revision_id='r-2'")
        with self.assertRaises(GateBlocked):
            validate_new_copy(path, schema=6, expected_digest=manifest["digest"])

    def test_changed_revision_lineage_rejected(self):
        path, manifest = self.fresh()
        with closing(sqlite3.connect(path)) as conn, conn:
            conn.execute("UPDATE scene_text_revisions SET previous_revision_id=NULL WHERE revision_id='r-2'")
        with self.assertRaises(GateBlocked):
            validate_new_copy(path, schema=6)

    def test_foreign_key_orphan_rejected(self):
        path, manifest = self.fresh()
        with closing(sqlite3.connect(path)) as conn, conn:
            conn.execute("PRAGMA foreign_keys=OFF")
            conn.execute("UPDATE narrative_facts SET universe_id='missing' WHERE fact_id='f-1'")
        with self.assertRaisesRegex(GateBlocked, "foreign key"):
            validate_new_copy(path, schema=6)

    def test_corrupted_file_rejected(self):
        path, manifest = self.fresh()
        path.write_bytes(b"not-a-sqlite-file")
        with self.assertRaises(GateBlocked):
            validate_new_copy(path, schema=6)

    def test_no_unknown_filename(self):
        with self.assertRaisesRegex(GateBlocked, "not authorized"):
            new_reserved_file(self.root / "backup", "operator.sqlite")

    def test_unexpected_table_rejected(self):
        path, manifest = self.fresh()
        with closing(sqlite3.connect(path)) as conn, conn:
            conn.execute("CREATE TABLE surprise (x INTEGER)")
        with self.assertRaisesRegex(GateBlocked, "unexpected table"):
            validate_new_copy(path, schema=6)

    def test_manifest_counts_mismatch(self):
        path, manifest = self.fresh()
        wrong = dict(manifest["counts"])
        wrong["narrative_facts"] = 2
        with self.assertRaisesRegex(GateBlocked, "count manifest"):
            validate_new_copy(path, schema=6, expected_counts=wrong)

    def test_v7_prospective_fixture(self):
        other = self.root / "source" / "synthetic_source.sqlite"
        other.unlink()
        src = new_synthetic_source(self.root / "source", version=7)
        path, manifest = self.fresh()
        self.assertEqual(manifest["schema"], 7)
        self.assertEqual(manifest["counts"]["world_time_anchors"], 1)

    def test_no_forged_independent_claim(self):
        path, manifest = self.fresh()
        self.assertTrue(manifest["synthetic_only"])
        self.assertNotIn("independent_human_approved", manifest)


if __name__ == "__main__":
    unittest.main()
