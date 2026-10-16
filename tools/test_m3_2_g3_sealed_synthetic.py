"""All tests use temporary, intentionally fictitious SQLite only."""
import hashlib
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
from m3_2_g3_sealed_synthetic import (
    SyntheticGateBlocked, _make_synthetic_db, _snapshot_toy_to_bytes,
    _exclusive_write_once, synthetic_trial,
)


class SealedToyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fabulaxiom-g3-test-")
        self.root = Path(self.temp.name)
        self.out = self.root / "new_dest"
        self.out.mkdir(mode=0o700)
        self.source = _make_synthetic_db(self.root, 6)
        self.payload = _snapshot_toy_to_bytes(self.source)

    def tearDown(self):
        self.temp.cleanup()

    def test_v6_end_to_end(self):
        self.assertTrue(synthetic_trial(6)["synthetic_only"])

    def test_v7_end_to_end(self):
        self.assertTrue(synthetic_trial(7)["synthetic_only"])

    def test_only_new_stream(self):
        result = _exclusive_write_once(self.out / "snapshot.sqlite3", self.payload)
        self.assertEqual(result["sha256"], hashlib.sha256(self.payload).hexdigest())

    def test_preexisting_zero_bytes_never_overwritten(self):
        t = self.out / "snapshot.sqlite3"
        t.write_bytes(b"")
        with self.assertRaisesRegex(SyntheticGateBlocked, "collision"):
            _exclusive_write_once(t, self.payload)
        self.assertEqual(t.read_bytes(), b"")

    def test_preexisting_sentinel_never_overwritten(self):
        t = self.out / "snapshot.sqlite3"
        t.write_bytes(b"DO NOT TOUCH")
        with self.assertRaisesRegex(SyntheticGateBlocked, "collision"):
            _exclusive_write_once(t, self.payload)
        self.assertEqual(t.read_bytes(), b"DO NOT TOUCH")

    def test_existing_directory_creation_rejected(self):
        with self.assertRaises(FileExistsError):
            self.out.mkdir(exist_ok=False)

    def test_wrong_basename_rejected(self):
        with self.assertRaises(SyntheticGateBlocked):
            _exclusive_write_once(self.out / "original.sqlite3", self.payload)

    def test_invalid_image_rejected_without_new_file(self):
        t = self.out / "snapshot.sqlite3"
        with self.assertRaises(SyntheticGateBlocked):
            _exclusive_write_once(t, b"not sqlite")
        self.assertFalse(t.exists())

    def test_missing_parent_not_created(self):
        t = self.root / "missing" / "snapshot.sqlite3"
        with self.assertRaises(SyntheticGateBlocked):
            _exclusive_write_once(t, self.payload)
        self.assertFalse(t.parent.exists())

    def test_memory_limit_rejects(self):
        with self.assertRaisesRegex(SyntheticGateBlocked, "memory budget"):
            _snapshot_toy_to_bytes(self.source, limit=1)

    def test_unknown_source_name_rejected(self):
        with self.assertRaisesRegex(SyntheticGateBlocked, "not a permitted"):
            _snapshot_toy_to_bytes(self.root / "not-operator.sqlite3")

    def test_unknown_schema_rejected(self):
        with self.assertRaises(SyntheticGateBlocked):
            synthetic_trial(8)

    def test_migration_registry_is_not_user_version(self):
        with closing(sqlite3.connect(self.source)) as db:
            self.assertEqual(db.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0], 6)
            self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 0)

    def test_symlinked_parent_refused_when_supported(self):
        link = self.root / "link"
        try:
            link.symlink_to(self.out, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Windows symlink privilege unavailable")
        with self.assertRaises(SyntheticGateBlocked):
            _exclusive_write_once(link / "snapshot.sqlite3", self.payload)


if __name__ == "__main__":
    unittest.main()
