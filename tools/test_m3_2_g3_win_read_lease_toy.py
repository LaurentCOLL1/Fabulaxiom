"""Windows G3 original-source read-lease qualification: toy files ONLY."""
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

from m3_2_g3_win_read_lease_toy import (
    ERROR_SHARING_VIOLATION, PREFIX, TOY_NAME, ToySafetyStop,
    _ancestors_and_role, _sidecars, _toy_v6, _windows_read_lease,
    header_info, toy_guarded_audit, write_open_while_lease,
)


class ToyLeaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=PREFIX)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = _toy_v6(self.root)

    def test_header_rollback_and_migration_identity_separate(self):
        h = header_info(self.source)
        self.assertEqual(h["journal"], 1)
        self.assertEqual(h["user_version"], 0)
        with closing(sqlite3.connect(self.source)) as db:
            self.assertEqual(db.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0], 6)

    @unittest.skipUnless(os.name == "nt", "Win32 lease is Windows-only")
    def test_read_lease_complete_toy_audit(self):
        result = toy_guarded_audit(self.root, self.source)
        self.assertEqual(result["status"], "TOY_ONLY_PASS")

    @unittest.skipUnless(os.name == "nt", "Win32 sharing is Windows-only")
    def test_read_lease_blocks_write_open(self):
        with _windows_read_lease(self.source):
            error = write_open_while_lease(self.source)
            self.assertEqual(error, ERROR_SHARING_VIOLATION)

    @unittest.skipUnless(os.name == "nt", "Win32 sharing is Windows-only")
    def test_existing_writer_blocks_read_lease(self):
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        f = kernel.CreateFileW
        f.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                      ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        f.restype = wintypes.HANDLE
        h = f(str(self.source), 0x40000000, 0x1 | 0x2, None, 3, 0x80, None)
        if h in (None, ctypes.c_void_p(-1).value):
            self.fail("cannot open disposable writer fixture")
        try:
            with self.assertRaisesRegex(ToySafetyStop, "read lease refused"):
                with _windows_read_lease(self.source):
                    pass
        finally:
            kernel.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel.CloseHandle(h)

    def test_hot_journal_sentinel_refused_before_sqlite(self):
        journal = Path(str(self.source) + "-journal")
        journal.write_bytes(b"TOY HOT JOURNAL SENTINEL")
        with self.assertRaisesRegex(ToySafetyStop, "sidecar"):
            _sidecars(self.source)
        if os.name == "nt":
            with self.assertRaisesRegex(ToySafetyStop, "sidecar"):
                toy_guarded_audit(self.root, self.source)

    def test_wal_header_refused_even_without_sidecars(self):
        with closing(sqlite3.connect(self.source)) as db:
            self.assertEqual(db.execute("PRAGMA journal_mode=WAL").fetchone()[0].lower(), "wal")
        self.assertEqual(self.source.read_bytes()[18:20], b"\x02\x02")
        with self.assertRaisesRegex(ToySafetyStop, "WAL/unknown"):
            header_info(self.source)

    def test_invalid_magic_refused(self):
        with self.source.open("r+b") as stream:
            stream.seek(0)
            stream.write(b"X")
        with self.assertRaisesRegex(ToySafetyStop, "magic"):
            header_info(self.source)

    def test_missing_source_rejected(self):
        self.source.unlink()
        with self.assertRaisesRegex(ToySafetyStop, "missing"):
            _ancestors_and_role(self.root, self.source)

    def test_unrecognized_filename_rejected(self):
        renamed = self.root / "operator.sqlite3"
        self.source.rename(renamed)
        with self.assertRaisesRegex(ToySafetyStop, "not a synthetic"):
            _ancestors_and_role(self.root, renamed)

    def test_invalid_fixture_root_rejected(self):
        with self.assertRaisesRegex(ToySafetyStop, "not a synthetic"):
            _ancestors_and_role(self.root.parent, self.source)

    def test_symlinked_source_rejected_if_possible(self):
        real = self.root / "other-toy.sqlite3"
        self.source.rename(real)
        try:
            self.source.symlink_to(real)
        except (OSError, NotImplementedError):
            self.skipTest("OS denies symlink creation")
        with self.assertRaisesRegex(ToySafetyStop, "reparse"):
            _ancestors_and_role(self.root, self.source)

    def test_source_is_fictional_and_contains_no_real_app_schema(self):
        with closing(sqlite3.connect(self.source)) as db:
            tables = [x[0] for x in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )]
        self.assertEqual(tables, ["imaginary_events", "schema_migrations"])


if __name__ == "__main__":
    unittest.main()
