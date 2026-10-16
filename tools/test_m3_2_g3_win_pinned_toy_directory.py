"""Win32 fixture-only parent directory pin / rename refusal tests."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest import mock

import m3_2_g3_win_pinned_toy_directory as module
from m3_2_g3_win_single_handle_toy import (
    TOY_PREFIX, ToyGateError, _locked_read_handle, create_fictional_toy,
)
from m3_2_g3_win_pinned_toy_directory import (
    pinned_toy_directory, inspect_under_pinned_toy_root, self_test
)


@unittest.skipUnless(os.name == "nt", "Requires Win32 handle sharing")
class PinnedToyDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix=TOY_PREFIX)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = create_fictional_toy(self.root, 6)

    def test_v6_v7_single_handle_trial(self):
        self_test()

    def test_holds_directory_identity_across_source_read(self):
        before = self.source.read_bytes()
        result = inspect_under_pinned_toy_root(self.root, self.source, version=6)
        self.assertEqual(result["status"], "TOY_ONLY_PASS")
        self.assertTrue(result["directory_identity"])
        self.assertTrue(result["source_identity"])
        self.assertEqual(before, self.source.read_bytes())

    def test_directory_rename_refused_or_detected(self):
        renamed = self.root.with_name(self.root.name + "-moved")
        moved = False
        try:
            with pinned_toy_directory(self.root):
                try:
                    os.rename(self.root, renamed)
                except OSError:
                    pass
                else:
                    moved = True
                    with self.assertRaisesRegex(ToyGateError, "directory missing"):
                        module._toy_directory_path_identity(self.root)
        finally:
            if moved and renamed.exists():
                os.rename(renamed, self.root)
        self.assertTrue(self.root.is_dir())
        self.assertFalse(renamed.exists())

    def test_source_handle_refuses_rename(self):
        moved = self.root / "other.sqlite3"
        with pinned_toy_directory(self.root):
            with _locked_read_handle(self.source):
                with self.assertRaises(OSError):
                    os.rename(self.source, moved)
        self.assertTrue(self.source.exists())
        self.assertFalse(moved.exists())

    def test_injected_directory_rename_refused_or_detected(self):
        renamed = self.root.with_name(self.root.name + "-hijacked")
        moved = False
        def attempt(root, _):
            nonlocal moved
            try:
                os.rename(root, renamed)
            except OSError:
                return
            moved = True
        result = None
        error = None
        try:
            try:
                result = inspect_under_pinned_toy_root(
                    self.root, self.source, version=6, test_hook=attempt
                )
            except ToyGateError as exc:
                error = exc
        finally:
            if moved and renamed.exists():
                os.rename(renamed, self.root)
        if moved:
            self.assertIsNotNone(error, "rename was not detected")
        else:
            self.assertIsNone(error)
            self.assertEqual(result["status"], "TOY_ONLY_PASS")

    def test_directory_identity_mismatch_fails_closed(self):
        real = module._toy_directory_path_identity
        calls = [0]
        def mismatched(root):
            calls[0] += 1
            observed = real(root)
            if calls[0] == 2:
                return (123456,) + tuple(observed[1:])
            return observed
        with mock.patch.object(module, "_toy_directory_path_identity", side_effect=mismatched):
            with self.assertRaisesRegex(ToyGateError, "pathname mismatch"):
                inspect_under_pinned_toy_root(self.root, self.source, version=6)

    def test_wrong_migration_fails(self):
        with self.assertRaisesRegex(ToyGateError, "schema_migrations mismatch"):
            inspect_under_pinned_toy_root(self.root, self.source, version=7)

    def test_journal_sentinel_fails(self):
        Path(str(self.source) + "-journal").write_bytes(b"toy sentinel")
        with self.assertRaisesRegex(ToyGateError, "sidecar"):
            inspect_under_pinned_toy_root(self.root, self.source, version=6)

    def test_root_symlink_fails_if_permitted(self):
        alias = self.root.parent / (self.root.name + "-link")
        try:
            alias.symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Windows symlink unavailable")
        self.addCleanup(lambda: alias.unlink(missing_ok=True))
        with self.assertRaises(ToyGateError):
            inspect_under_pinned_toy_root(alias, alias / self.source.name, version=6)

    def test_source_symlink_fails_if_permitted(self):
        other = self.root / "original.sqlite3"
        self.source.rename(other)
        try:
            self.source.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest("Windows symlink unavailable")
        with self.assertRaisesRegex(ToyGateError, "reparse|symlink"):
            inspect_under_pinned_toy_root(self.root, self.source, version=6)

    def test_outside_runtime_temp_root_fails(self):
        invalid = self.root / "nested"
        invalid.mkdir()
        bogus = invalid / self.source.name
        with self.assertRaises(ToyGateError):
            inspect_under_pinned_toy_root(invalid, bogus, version=6)

    def test_missing_toy_source_fails(self):
        self.source.unlink()
        with self.assertRaisesRegex(ToyGateError, "missing"):
            inspect_under_pinned_toy_root(self.root, self.source, version=6)

    def test_existing_writer_conflicts_with_source_read_handle(self):
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        f = kernel.CreateFileW
        f.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                      ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        f.restype = wintypes.HANDLE
        h = f(str(self.source), 0x40000000, 0x3, None, 3, 0x80, None)
        self.assertNotIn(h, (None, ctypes.c_void_p(-1).value))
        try:
            with self.assertRaisesRegex(ToyGateError, "readonly open denied"):
                inspect_under_pinned_toy_root(self.root, self.source, version=6)
        finally:
            kernel.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel.CloseHandle(h)


if __name__ == "__main__":
    unittest.main()
