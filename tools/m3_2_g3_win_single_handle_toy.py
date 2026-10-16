"""Win32 single-handle physical image -> in-memory SQLite: TOY ONLY.

No original SQLite file is ever opened by SQLite during acquisition. Fixtures
are invented and created under TemporaryDirectory by this module. The public
CLI allows --self-test only and no operator file path.

Not a general preservation utility: unsafe for real data, hot journals, WAL,
untrusted parent directory races or sources with active third-party writers.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
import ctypes
from ctypes import wintypes
import hashlib
import os
from pathlib import Path
import sqlite3
import stat
import tempfile

TOY_PREFIX = "fabulaxiom-m32-onehandle-toy-"
TOY_FILE = "fictional.sqlite3"
TOY_MAX_BYTES = 2 * 1024 * 1024
MAGIC = b"SQLite format 3\x00"
READ = 0x80000000
WRITE = 0x40000000
SHARE_READ = 0x00000001
SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
FILE_ATTRIBUTE_NORMAL = 0x00000080
ERROR_SHARING_VIOLATION = 32


class ToyGateError(RuntimeError):
    """Fail-closed toy fixture gate."""


class HandleFileInfo(ctypes.Structure):
    _fields_ = [
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", wintypes.FILETIME),
        ("ftLastAccessTime", wintypes.FILETIME),
        ("ftLastWriteTime", wintypes.FILETIME),
        ("dwVolumeSerialNumber", wintypes.DWORD),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
        ("nNumberOfLinks", wintypes.DWORD),
        ("nFileIndexHigh", wintypes.DWORD),
        ("nFileIndexLow", wintypes.DWORD),
    ]


def _bytes_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _toy_path(root: Path, path: Path) -> None:
    if not root.name.startswith(TOY_PREFIX) or path.name != TOY_FILE or path.parent != root:
        raise ToyGateError("not a declared disposable fixture role")
    for part in (root, path):
        try:
            meta = part.lstat()
        except OSError as exc:
            raise ToyGateError("missing toy root/source") from exc
        if stat.S_ISLNK(meta.st_mode) or getattr(meta, "st_file_attributes", 0) & FILE_ATTRIBUTE_REPARSE_POINT:
            raise ToyGateError("reparse/symlink toy role refused")
    if not root.is_dir() or not path.is_file():
        raise ToyGateError("toy role type invalid")


def _no_sidecars(path: Path) -> None:
    for suffix in ("-wal", "-shm", "-journal"):
        candidate = Path(str(path) + suffix)
        if candidate.exists() or candidate.is_symlink():
            raise ToyGateError("toy SQLite sidecar present")


def _check_image(image: bytes) -> int:
    if len(image) < 512 or image[:16] != MAGIC:
        raise ToyGateError("malformed SQLite toy image")
    p = int.from_bytes(image[16:18], "big")
    p = 65536 if p == 1 else p
    if not (512 <= p <= 65536) or p & (p - 1) or len(image) % p:
        raise ToyGateError("SQLite page alignment failed")
    if image[18:20] != b"\x01\x01":
        raise ToyGateError("WAL/unknown journal header forbidden")
    fmt = int.from_bytes(image[44:48], "big")
    if fmt not in (1, 2, 3, 4):
        raise ToyGateError("unknown SQLite format")
    # Header field is informative, NOT a Fabulaxiom migration registry.
    return p


def _identity(info: HandleFileInfo) -> tuple[int, ...]:
    return (
        int(info.dwVolumeSerialNumber),
        int(info.nFileIndexHigh),
        int(info.nFileIndexLow),
        int(info.nFileSizeHigh),
        int(info.nFileSizeLow),
        int(info.ftLastWriteTime.dwHighDateTime),
        int(info.ftLastWriteTime.dwLowDateTime),
        int(info.dwFileAttributes),
    )


def _get_file_info(kernel, handle: int) -> HandleFileInfo:
    getinfo = kernel.GetFileInformationByHandle
    getinfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(HandleFileInfo)]
    getinfo.restype = wintypes.BOOL
    obj = HandleFileInfo()
    if not getinfo(handle, ctypes.byref(obj)):
        raise ToyGateError(f"Win32 file-info failed: {ctypes.get_last_error()}")
    if int(obj.dwFileAttributes) & FILE_ATTRIBUTE_REPARSE_POINT:
        raise ToyGateError("Win32 reparse point refused")
    if not (int(obj.dwVolumeSerialNumber) or int(obj.nFileIndexHigh) or int(obj.nFileIndexLow)):
        raise ToyGateError("Win32 file identity unavailable")
    return obj


def _kernel():
    if os.name != "nt":
        raise ToyGateError("Win32-only synthetic experiment")
    return ctypes.WinDLL("kernel32", use_last_error=True)


@contextmanager
def _locked_read_handle(path: Path):
    kernel = _kernel()
    create = kernel.CreateFileW
    create.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE
    ]
    create.restype = wintypes.HANDLE
    handle = create(str(path), READ, SHARE_READ, None, OPEN_EXISTING,
                    FILE_FLAG_OPEN_REPARSE_POINT, None)
    if handle in (None, ctypes.c_void_p(-1).value):
        raise ToyGateError(f"Win32 readonly open denied: {ctypes.get_last_error()}")
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    close.restype = wintypes.BOOL
    try:
        yield kernel, handle
    finally:
        if not close(handle):
            raise ToyGateError("Win32 close failed")


def _read_full_image(kernel, handle: int, *, max_bytes: int) -> tuple[bytes, tuple[int, ...]]:
    if not 0 < max_bytes <= TOY_MAX_BYTES:
        raise ToyGateError("toy memory budget not authorized")
    start = _get_file_info(kernel, handle)
    length = (int(start.nFileSizeHigh) << 32) | int(start.nFileSizeLow)
    if length < 512 or length > max_bytes:
        raise ToyGateError("file outside toy memory budget")
    reader = kernel.ReadFile
    reader.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD,
                       ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    reader.restype = wintypes.BOOL
    pieces: list[bytes] = []
    remaining = length
    while remaining:
        n = min(remaining, 65536)
        buf = ctypes.create_string_buffer(n)
        count = wintypes.DWORD()
        if not reader(handle, buf, n, ctypes.byref(count), None):
            raise ToyGateError(f"Win32 ReadFile failed: {ctypes.get_last_error()}")
        if count.value == 0 or count.value > n:
            raise ToyGateError("truncated / invalid Win32 ReadFile")
        pieces.append(buf.raw[:count.value])
        remaining -= count.value
    end = _get_file_info(kernel, handle)
    if _identity(start) != _identity(end):
        raise ToyGateError("Win32 source identity changed while reading")
    content = b"".join(pieces)
    _check_image(content)
    return content, _identity(start)


def create_fictional_toy(root: Path, version: int) -> Path:
    if version not in (6, 7) or not root.name.startswith(TOY_PREFIX) or root.is_symlink():
        raise ToyGateError("not an allowed fictional fixture")
    path = root / TOY_FILE
    if path.exists() or path.is_symlink():
        raise ToyGateError("toy source collision")
    with closing(sqlite3.connect(path)) as conn, conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("CREATE TABLE imagined_books (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
        conn.execute("CREATE TABLE invented_facts (id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES imagined_books(id), detail TEXT NOT NULL)")
        conn.execute("CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        conn.execute("INSERT INTO imagined_books VALUES(1, 'Toy story')")
        conn.execute("INSERT INTO invented_facts VALUES(1, 1, 'Example')")
        for step in range(1, version + 1):
            conn.execute("INSERT INTO schema_migrations VALUES(?,?)", (step, f"toy_{step}"))
    return path


def inspect_memory_image(image: bytes, version: int) -> dict[str, object]:
    if not hasattr(sqlite3.Connection, "deserialize"):
        raise ToyGateError("SQLite deserialize API not available")
    _check_image(image)
    if version not in (6, 7):
        raise ToyGateError("unknown toy migration level")
    try:
        with closing(sqlite3.connect(":memory:")) as conn:
            conn.deserialize(image)
            conn.execute("PRAGMA query_only=ON")
            if conn.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise ToyGateError("in-memory integrity_check failure")
            if conn.execute("PRAGMA foreign_key_check").fetchall():
                raise ToyGateError("in-memory foreign_key_check failure")
            rows = conn.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall()
            if rows != [(i,) for i in range(1, version+1)]:
                raise ToyGateError("toy schema_migrations mismatch")
            if conn.execute("SELECT count(*) FROM imagined_books").fetchone()[0] != 1:
                raise ToyGateError("toy books mismatch")
            if conn.execute("SELECT count(*) FROM invented_facts").fetchone()[0] != 1:
                raise ToyGateError("toy facts mismatch")
    except sqlite3.DatabaseError as exc:
        raise ToyGateError("malformed or inconsistent in-memory SQLite") from exc
    return {"version": version, "sha256": _bytes_digest(image),
            "bytes": len(image), "in_memory_only": True}


def acquire_toy(root: Path, source: Path, *, version: int, max_bytes: int = TOY_MAX_BYTES):
    """Source opened only with a Win32 handle; sqlite3 touches RAM image ONLY."""
    _toy_path(root, source)
    _no_sidecars(source)
    with _locked_read_handle(source) as (kernel, handle):
        _toy_path(root, source)
        _no_sidecars(source)
        image, file_id = _read_full_image(kernel, handle, max_bytes=max_bytes)
        report = inspect_memory_image(image, version)
        _no_sidecars(source)
        # Same retained handle is still open at this point. The toy parent
        # directory remains susceptible to namespace races.
        if file_id != _identity(_get_file_info(kernel, handle)):
            raise ToyGateError("file identity changed after memory validation")
    _no_sidecars(source)
    return image, dict(report, win32_file_id_observed=bool(file_id))


def self_test() -> None:
    for version in (6, 7):
        with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as tmp:
            root = Path(tmp)
            src = create_fictional_toy(root, version)
            before = src.read_bytes()
            image, status = acquire_toy(root, src, version=version)
            if image != before or src.read_bytes() != before or status["version"] != version:
                raise ToyGateError("toy source or in-memory image unexpectedly changed")
    print("M3.2 WIN32 SINGLE HANDLE TOY: PASS (no operator files)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Win32 toy single-handle audit only")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("Only --self-test; no operator source/target options")
    self_test()
