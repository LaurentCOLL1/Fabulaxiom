"""Win32-only synthetic capture -> sealed destination -> third-location restore."""
from contextlib import closing
import hashlib
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

from m3_2_g3_win_single_handle_toy import TOY_PREFIX, TOY_FILE, ToyGateError, create_fictional_toy
from m3_2_g3_win_full_toy_cycle import (
    SNAPSHOT_DIR, RESTORE_DIR, SNAPSHOT_NAME, ToyCeremonyVeto,
    capture_toy, _new_dir, _write_new_snapshot, _assert_copy,
    restore_toy, full_toy_cycle
)


@unittest.skipUnless(os.name == "nt", "Windows-only toy Win32 handles")
class Win32FullToyCycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix=TOY_PREFIX)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = create_fictional_toy(self.root, 6)

    def test_sealed_capture_restore_v6(self):
        # full_toy_cycle owns creation, use a distinct disposable fixture.
        with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as location:
            result = full_toy_cycle(Path(location), 6)
            self.assertFalse(result["real_g3_authorized"])
            self.assertEqual(result["snapshot_sha256"], result["restore_sha256"])
            self.assertEqual(result["scope"], "FICTIONAL_TOY_ONLY")

    def test_sealed_capture_restore_v7(self):
        with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as location:
            result = full_toy_cycle(Path(location), 7)
            self.assertEqual(result["version"], 7)
            self.assertEqual(result["transient_ancestor_swap_resistance"], "UNPROVEN")

    def test_capture_without_real_sqlite_reopen(self):
        baseline = self.source.read_bytes()
        image, proof = capture_toy(self.root, version=6)
        self.assertEqual(image, baseline)
        self.assertTrue(proof["source_identity"])
        self.assertFalse((self.root / SNAPSHOT_DIR).exists())

    def test_sole_directory_name_must_be_new(self):
        d = _new_dir(self.root, SNAPSHOT_DIR)
        with self.assertRaisesRegex(ToyCeremonyVeto, "collision"):
            _new_dir(self.root, SNAPSHOT_DIR)
        self.assertTrue(d.is_dir())

    def test_preexisting_empty_file_preserved(self):
        image, _ = capture_toy(self.root, version=6)
        d = _new_dir(self.root, SNAPSHOT_DIR)
        f = d / SNAPSHOT_NAME
        f.write_bytes(b"")
        with self.assertRaisesRegex(ToyCeremonyVeto, "exclusive"):
            _write_new_snapshot(d, image)
        self.assertEqual(f.read_bytes(), b"")

    def test_preexisting_sentinel_preserved(self):
        image, _ = capture_toy(self.root, version=6)
        d = _new_dir(self.root, SNAPSHOT_DIR)
        f = d / SNAPSHOT_NAME
        f.write_bytes(b"EXISTING TOY DATA")
        with self.assertRaises(ToyCeremonyVeto):
            _write_new_snapshot(d, image)
        self.assertEqual(f.read_bytes(), b"EXISTING TOY DATA")

    def test_restoration_destination_collision_not_overwritten(self):
        image, _ = capture_toy(self.root, version=6)
        d = _new_dir(self.root, SNAPSHOT_DIR)
        _write_new_snapshot(d, image)
        restored = _new_dir(self.root, RESTORE_DIR)
        (restored / SNAPSHOT_NAME).write_bytes(b"DO NOT TOUCH")
        with self.assertRaisesRegex(ToyCeremonyVeto, "collision"):
            restore_toy(self.root, image, 6)
        self.assertEqual((restored / SNAPSHOT_NAME).read_bytes(), b"DO NOT TOUCH")

    def test_corrupted_snapshot_refuses_restore_without_new_dir(self):
        image, _ = capture_toy(self.root, version=6)
        d = _new_dir(self.root, SNAPSHOT_DIR)
        _write_new_snapshot(d, image)
        f = d / SNAPSHOT_NAME
        content = bytearray(f.read_bytes())
        content[-1] ^= 0xFF
        f.write_bytes(content)
        with self.assertRaisesRegex(ToyCeremonyVeto, "mutated"):
            restore_toy(self.root, image, 6)
        self.assertFalse((self.root / RESTORE_DIR).exists())

    def test_restored_copy_has_exact_bytes_and_schema(self):
        image, _ = capture_toy(self.root, version=6)
        d = _new_dir(self.root, SNAPSHOT_DIR)
        _write_new_snapshot(d, image)
        result = restore_toy(self.root, image, 6)
        path = self.root / RESTORE_DIR / SNAPSHOT_NAME
        self.assertEqual(path.read_bytes(), image)
        self.assertEqual(result["sha256"], hashlib.sha256(image).hexdigest())
        with closing(sqlite3.connect(":memory:")) as db:
            db.deserialize(path.read_bytes())
            self.assertEqual(db.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0], 6)

    def test_wrong_migration_rejected_before_snapshot(self):
        with self.assertRaisesRegex(ToyGateError, "schema_migrations mismatch"):
            capture_toy(self.root, version=7)
        self.assertFalse((self.root / SNAPSHOT_DIR).exists())

    def test_fk_corruption_rejected_before_snapshot(self):
        with closing(sqlite3.connect(self.source)) as db, db:
            db.execute("PRAGMA foreign_keys=OFF")
            db.execute("UPDATE invented_facts SET book_id=999 WHERE id=1")
        with self.assertRaisesRegex(ToyGateError, "foreign_key_check"):
            capture_toy(self.root, version=6)
        self.assertFalse((self.root / SNAPSHOT_DIR).exists())

    def test_hot_journal_sentinel_refuses_capture(self):
        Path(str(self.source) + "-journal").write_bytes(b"SYNTHETIC JOURNAL")
        with self.assertRaisesRegex(ToyGateError, "sidecar"):
            capture_toy(self.root, version=6)
        self.assertFalse((self.root / SNAPSHOT_DIR).exists())

    def test_wal_header_refuses_capture(self):
        with closing(sqlite3.connect(self.source)) as db:
            db.execute("PRAGMA journal_mode=WAL")
        with self.assertRaisesRegex(ToyGateError, "WAL/unknown"):
            capture_toy(self.root, version=6)
        self.assertFalse((self.root / SNAPSHOT_DIR).exists())

    def test_wrong_memory_budget_refuses_preflight(self):
        with self.assertRaisesRegex(ToyCeremonyVeto, "memory cap"):
            capture_toy(self.root, version=6, max_size=1)
        self.assertFalse((self.root / SNAPSHOT_DIR).exists())

    def test_missing_snapshot_refuses_restoration(self):
        image, _ = capture_toy(self.root, version=6)
        with self.assertRaisesRegex(ToyCeremonyVeto, "missing"):
            restore_toy(self.root, image, 6)
        self.assertFalse((self.root / RESTORE_DIR).exists())

    def test_no_real_authority_and_transient_swap_limitation(self):
        with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as location:
            verdict = full_toy_cycle(Path(location), 6)
            self.assertEqual(verdict["transient_ancestor_swap_resistance"], "UNPROVEN")
            self.assertFalse(verdict["real_g3_authorized"])


if __name__ == "__main__":
    unittest.main()
