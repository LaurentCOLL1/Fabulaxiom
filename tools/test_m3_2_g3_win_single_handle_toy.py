"""All tests generate and dispose of fictitious SQLite. Never open operator DBs."""
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

from m3_2_g3_win_single_handle_toy import (
    TOY_PREFIX, TOY_MAX_BYTES, ToyGateError, _locked_read_handle, _read_full_image,
    _toy_path, _no_sidecars, acquire_toy, create_fictional_toy,
    inspect_memory_image, self_test
)


@unittest.skipUnless(os.name == "nt", "Win32-only experimental source guard")
class SingleHandleWindowsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=TOY_PREFIX)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = create_fictional_toy(self.root, 6)

    def test_entire_pipeline_v6_and_v7(self):
        self_test()

    def test_source_image_identical_and_stable(self):
        expected = self.source.read_bytes()
        image, verdict = acquire_toy(self.root, self.source, version=6)
        self.assertEqual(image, expected)
        self.assertEqual(self.source.read_bytes(), expected)
        self.assertTrue(verdict["win32_file_id_observed"])
        self.assertEqual(verdict["bytes"], len(expected))

    def test_existing_writer_refuses_handle(self):
        from ctypes import wintypes
        import ctypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        create = kernel.CreateFileW
        create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                           ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        create.restype = wintypes.HANDLE
        writer = create(str(self.source), 0x40000000, 0x1 | 0x2, None, 3, 0x80, None)
        self.assertNotIn(writer, (None, ctypes.c_void_p(-1).value))
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        try:
            with self.assertRaisesRegex(ToyGateError, "readonly open denied"):
                acquire_toy(self.root, self.source, version=6)
        finally:
            kernel.CloseHandle(writer)

    def test_second_writer_refused_under_read_handle(self):
        from m3_2_g3_win_read_lease_toy import write_open_while_lease, ERROR_SHARING_VIOLATION
        with _locked_read_handle(self.source):
            self.assertEqual(write_open_while_lease(self.source), ERROR_SHARING_VIOLATION)

    def test_wrong_migration_rejected(self):
        with self.assertRaisesRegex(ToyGateError, "schema_migrations mismatch"):
            acquire_toy(self.root, self.source, version=7)

    def test_existing_journal_sentinel_rejected(self):
        Path(str(self.source) + "-journal").write_bytes(b"toy-journal")
        with self.assertRaisesRegex(ToyGateError, "sidecar"):
            acquire_toy(self.root, self.source, version=6)

    def test_existing_wal_sentinel_rejected(self):
        Path(str(self.source) + "-wal").write_bytes(b"toy-wal")
        with self.assertRaisesRegex(ToyGateError, "sidecar"):
            acquire_toy(self.root, self.source, version=6)

    def test_wal_header_without_sidecars_rejected(self):
        with closing(sqlite3.connect(self.source)) as db:
            self.assertEqual(db.execute("PRAGMA journal_mode=WAL").fetchone()[0].lower(), "wal")
        with self.assertRaisesRegex(ToyGateError, "WAL/unknown"):
            acquire_toy(self.root, self.source, version=6)

    def test_short_memory_budget_rejected(self):
        with self.assertRaisesRegex(ToyGateError, "memory budget"):
            acquire_toy(self.root, self.source, version=6, max_bytes=4096)

    def test_malformed_header_rejected(self):
        with self.source.open("r+b") as stream:
            stream.write(b"BAD")
        with self.assertRaisesRegex(ToyGateError, "malformed SQLite"):
            acquire_toy(self.root, self.source, version=6)

    def test_foreign_key_failure_in_ram_rejected(self):
        with closing(sqlite3.connect(self.source)) as db, db:
            db.execute("PRAGMA foreign_keys=OFF")
            db.execute("UPDATE invented_facts SET book_id=999 WHERE id=1")
        with self.assertRaisesRegex(ToyGateError, "foreign_key_check"):
            acquire_toy(self.root, self.source, version=6)

    def test_original_source_symlink_rejected_if_allowed(self):
        elsewhere = self.root / "real-toy.sqlite3"
        self.source.rename(elsewhere)
        try:
            self.source.symlink_to(elsewhere)
        except (OSError, NotImplementedError):
            self.skipTest("Windows symlink permission unavailable")
        with self.assertRaisesRegex(ToyGateError, "symlink"):
            acquire_toy(self.root, self.source, version=6)

    def test_unexpected_file_role_rejected(self):
        rogue = self.root / "operator.sqlite3"
        self.source.rename(rogue)
        with self.assertRaisesRegex(ToyGateError, "not a declared"):
            acquire_toy(self.root, rogue, version=6)

    def test_deleted_source_rejected(self):
        self.source.unlink()
        with self.assertRaisesRegex(ToyGateError, "missing"):
            acquire_toy(self.root, self.source, version=6)

    def test_file_id_stable_within_same_handle(self):
        with _locked_read_handle(self.source) as (kernel, handle):
            image, before = _read_full_image(kernel, handle, max_bytes=TOY_MAX_BYTES)
            _, after = _read_full_image(kernel, handle, max_bytes=TOY_MAX_BYTES)
            self.assertEqual(before, after)
            self.assertEqual(image[:16], b"SQLite format 3\x00")


if __name__ == "__main__":
    unittest.main()
