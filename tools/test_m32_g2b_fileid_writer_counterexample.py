"""M3.2 G2-B counterexamples on disposable invented bytes, CI ONLY.

This test module has no CLI accepting paths, no SQLite connection, no access to
operator data or application locations. Any filesystem I/O occurs strictly in
TemporaryDirectory on a GitHub Actions Windows runner. Nothing authorizes G2-C.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes
import os
from pathlib import Path
import tempfile
import unittest


READ_ATTRIBUTES = 0x80
GENERIC_WRITE = 0x40000000
SHARE_READ = 0x1
SHARE_WRITE = 0x2
SHARE_DELETE = 0x4
SHARE_ALL = SHARE_READ | SHARE_WRITE | SHARE_DELETE
OPEN_EXISTING = 3
OPEN_REPARSE_POINT = 0x00200000
FILE_ID_INFO_CLASS = 18
SHARING_VIOLATION = 32
TOY_PREFIX = "fabulaxiom-m32-g2b-metadata-toy-"
TOY_BYTES_BEFORE = b"FICTIVE1"
TOY_BYTES_AFTER = b"FICTIVE2"


def evidence_verdict(*, file_id_stable: bool, metadata_stable: bool,
                     marker_match: bool, sidecars_absent: bool,
                     sharing_allows_writes: bool) -> dict[str, object]:
    """All arguments are *hypothetical*, never evidence of operator custody."""
    args = (file_id_stable, metadata_stable, marker_match,
            sidecars_absent, sharing_allows_writes)
    if any(type(v) is not bool for v in args):
        raise TypeError("STOP: non-boolean fictional evidence")
    return {
        "source_identity": "PARTIAL_LOCAL_IDENTITY_ONLY",
        "process_writer_absence": "NOT_PROVEN",
        "historical_custody": "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
        "prospective_baseline": "NOT_STARTED",
        "g2c": "NOT_AUTHORIZED",
        "real_g3": "STOP_UNAVAILABLE",
        "real_g3_authorized": False,
    }


class FileIdInfo(ctypes.Structure):
    _fields_ = [("volume_serial", ctypes.c_uint64),
                ("file_id", ctypes.c_ubyte * 16)]


class WinApi:
    def __init__(self):
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.create = kernel.CreateFileW
        self.create.argtypes = [
            wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
        ]
        self.create.restype = wintypes.HANDLE
        self.close = kernel.CloseHandle
        self.close.argtypes = [wintypes.HANDLE]
        self.close.restype = wintypes.BOOL
        self.get_info = kernel.GetFileInformationByHandleEx
        self.get_info.argtypes = [
            wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
        ]
        self.get_info.restype = wintypes.BOOL
        self.write = kernel.WriteFile
        self.write.argtypes = [
            wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p,
        ]
        self.write.restype = wintypes.BOOL
        self.flush = kernel.FlushFileBuffers
        self.flush.argtypes = [wintypes.HANDLE]
        self.flush.restype = wintypes.BOOL

    def open(self, path: Path, access: int, share: int) -> int:
        handle = self.create(str(path), access, share, None, OPEN_EXISTING,
                             OPEN_REPARSE_POINT, None)
        if handle in (None, ctypes.c_void_p(-1).value):
            raise OSError(ctypes.get_last_error(), "toy Windows CreateFileW refused")
        return handle

    def identity(self, handle: int) -> tuple[int, bytes]:
        value = FileIdInfo()
        if not self.get_info(handle, FILE_ID_INFO_CLASS, ctypes.byref(value),
                             ctypes.sizeof(value)):
            raise OSError(ctypes.get_last_error(), "toy FileIdInfo failed")
        return value.volume_serial, bytes(value.file_id)


class ModelCounterexamples(unittest.TestCase):
    def test_01_all_positive_metadata_still_refuses(self):
        x = evidence_verdict(file_id_stable=True, metadata_stable=True,
                             marker_match=True, sidecars_absent=True,
                             sharing_allows_writes=True)
        self.assertEqual(x["process_writer_absence"], "NOT_PROVEN")
        self.assertEqual(x["g2c"], "NOT_AUTHORIZED")
        self.assertEqual(x["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(x["real_g3_authorized"])

    def test_02_stronger_hypothetical_sharing_does_not_authorize(self):
        x = evidence_verdict(file_id_stable=True, metadata_stable=True,
                             marker_match=True, sidecars_absent=True,
                             sharing_allows_writes=False)
        self.assertEqual(x["source_identity"], "PARTIAL_LOCAL_IDENTITY_ONLY")
        self.assertFalse(x["real_g3_authorized"])

    def test_03_false_or_missing_observations_still_refuse(self):
        x = evidence_verdict(file_id_stable=False, metadata_stable=False,
                             marker_match=False, sidecars_absent=False,
                             sharing_allows_writes=True)
        self.assertEqual(x["prospective_baseline"], "NOT_STARTED")
        self.assertEqual(x["historical_custody"], "PENDING_EXTERNAL_ATTESTATION(21/3/2)")

    def test_04_integer_not_accepted_as_boolean(self):
        with self.assertRaisesRegex(TypeError, "STOP"):
            evidence_verdict(file_id_stable=1, metadata_stable=True,
                             marker_match=True, sidecars_absent=True,
                             sharing_allows_writes=True)


@unittest.skipUnless(os.name == "nt" and os.getenv("GITHUB_ACTIONS") == "true",
                     "real Win32 toy handles execute only on GitHub Actions Windows")
class WindowsScratchCounterexamples(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=TOY_PREFIX)
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "fictional-bytes.bin"
        self.assertTrue(Path(self.temp.name).name.startswith(TOY_PREFIX))
        self.file.write_bytes(TOY_BYTES_BEFORE)
        self.api = WinApi()

    def test_05_share_all_permits_second_writer_open(self):
        metadata = self.api.open(self.file, READ_ATTRIBUTES, SHARE_ALL)
        try:
            writer = self.api.open(self.file, GENERIC_WRITE, SHARE_ALL)
            self.assertTrue(writer)
            self.assertTrue(self.api.close(writer))
        finally:
            self.assertTrue(self.api.close(metadata))

    def test_06_same_file_id_can_have_different_bytes_under_share_all(self):
        metadata = self.api.open(self.file, READ_ATTRIBUTES, SHARE_ALL)
        try:
            before_id = self.api.identity(metadata)
            self.assertNotEqual(before_id[1], bytes(16))
            writer = self.api.open(self.file, GENERIC_WRITE, SHARE_ALL)
            try:
                buffer = ctypes.create_string_buffer(TOY_BYTES_AFTER)
                written = wintypes.DWORD()
                if not self.api.write(writer, buffer, len(TOY_BYTES_AFTER),
                                      ctypes.byref(written), None):
                    raise OSError(ctypes.get_last_error(), "toy WriteFile failed")
                self.assertEqual(written.value, len(TOY_BYTES_AFTER))
                self.assertTrue(self.api.flush(writer))
            finally:
                self.assertTrue(self.api.close(writer))
            after_id = self.api.identity(metadata)
            self.assertEqual(before_id, after_id,
                             "same volume/FileId despite synthetic mutation")
            self.assertEqual(self.file.read_bytes(), TOY_BYTES_AFTER)
        finally:
            self.assertTrue(self.api.close(metadata))

    def test_07_existing_writer_is_compatible_with_share_all_monitor(self):
        writer = self.api.open(self.file, GENERIC_WRITE, SHARE_ALL)
        try:
            metadata = self.api.open(self.file, READ_ATTRIBUTES, SHARE_ALL)
            try:
                self.assertNotEqual(self.api.identity(metadata)[1], bytes(16))
            finally:
                self.assertTrue(self.api.close(metadata))
        finally:
            self.assertTrue(self.api.close(writer))

    def test_08_attribute_only_share_read_does_not_exclude_writer(self):
        # Windows CI demonstrated that an attribute-only handle does not
        # establish a writer-exclusion lease, even without SHARE_WRITE.
        monitor = self.api.open(self.file, READ_ATTRIBUTES, SHARE_READ)
        try:
            before = self.api.identity(monitor)
            writer = self.api.open(self.file, GENERIC_WRITE, SHARE_ALL)
            try:
                self.assertTrue(writer)
            finally:
                self.assertTrue(self.api.close(writer))
            self.assertEqual(self.api.identity(monitor), before)
        finally:
            self.assertTrue(self.api.close(monitor))


if __name__ == "__main__":
    unittest.main()
