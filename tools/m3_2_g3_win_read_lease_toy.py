"""M3.2 Windows READ LEASE EXPERIMENT: DISPOSABLE TOY DATABASES ONLY.

No operator source/destination CLI, no original-file API. The Windows share
lease is an experimental negative-control for competing WRITE opens, NOT a
proof that arbitrary operator files or their parent directories are safe.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
import ctypes
import hashlib
import os
from pathlib import Path
import sqlite3
import stat
import tempfile


class ToySafetyStop(RuntimeError):
    """A mandatory condition for the disposable toy was not met."""


MAGIC = b"SQLite format 3\x00"
TOY_NAME = "synthetic-guard.sqlite3"
PREFIX = "fabulaxiom-m32-source-toy-"
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2
OPEN_EXISTING = 3
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_ATTRIBUTE_NORMAL = 0x80
ERROR_SHARING_VIOLATION = 32
REPARSE_ATTRIBUTE = 0x400


def _digest(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def _sidecars(source: Path) -> None:
    for suffix in ("-wal", "-shm", "-journal"):
        if Path(str(source) + suffix).exists() or Path(str(source) + suffix).is_symlink():
            raise ToySafetyStop("sidecar detected: must not open toy SQLite")


def _ancestors_and_role(root: Path, source: Path) -> None:
    # Do not resolve a path that may cross a symlink before checking attributes.
    if not root.name.startswith(PREFIX) or source.name != TOY_NAME:
        raise ToySafetyStop("not a synthetic source role")
    if source.parent != root:
        raise ToySafetyStop("toy source outside supplied root")
    for p in (root, source):
        try:
            meta = p.lstat()
        except OSError as exc:
            raise ToySafetyStop("toy source/root missing") from exc
        if stat.S_ISLNK(meta.st_mode) or getattr(meta, "st_file_attributes", 0) & REPARSE_ATTRIBUTE:
            raise ToySafetyStop("toy reparse point")
    if not root.is_dir() or not source.is_file():
        raise ToySafetyStop("invalid toy source type")


def header_info(path: Path) -> dict[str, int]:
    with path.open("rb") as inp:
        raw = inp.read(100)
    if len(raw) != 100 or raw[:16] != MAGIC:
        raise ToySafetyStop("invalid SQLite magic/header")
    page = int.from_bytes(raw[16:18], "big")
    page = 65536 if page == 1 else page
    if page < 512 or page > 65536 or page & (page - 1):
        raise ToySafetyStop("invalid toy page size")
    if path.stat().st_size % page:
        raise ToySafetyStop("page alignment failed")
    read_version, write_version = raw[19], raw[18]
    if read_version != 1 or write_version != 1:
        raise ToySafetyStop("WAL/unknown journal header refused")
    format_number = int.from_bytes(raw[44:48], "big")
    if format_number not in (1, 2, 3, 4):
        raise ToySafetyStop("invalid schema format")
    return {"page_size": page, "user_version": int.from_bytes(raw[60:64], "big"),
            "format": format_number, "journal": 1}


@contextmanager
def _windows_read_lease(source: Path):
    """Hold a Windows READ handle with FILE_SHARE_READ, never SHARE_WRITE.

    This is only a toy experiment. Share-mode blocks compatible file opens;
    it does not atomically lock all directory names or establish authentic
    custody of a historical file.
    """
    if os.name != "nt":
        raise ToySafetyStop("Windows-only lease experiment")
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    make = kernel.CreateFileW
    make.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                     ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
                     wintypes.HANDLE]
    make.restype = wintypes.HANDLE
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    close.restype = wintypes.BOOL
    handle = make(str(source), GENERIC_READ, FILE_SHARE_READ, None,
                  OPEN_EXISTING, FILE_FLAG_OPEN_REPARSE_POINT, None)
    invalid = ctypes.c_void_p(-1).value
    if handle in (None, invalid):
        raise ToySafetyStop("Windows read lease refused: error=" + str(ctypes.get_last_error()))
    try:
        yield handle
    finally:
        if not close(handle):
            raise ToySafetyStop("Windows read lease close failure")


def _toy_v6(root: Path) -> Path:
    if not root.name.startswith(PREFIX) or not root.is_dir() or root.is_symlink():
        raise ToySafetyStop("invalid toy root")
    source = root / TOY_NAME
    if source.exists() or source.is_symlink():
        raise ToySafetyStop("toy already exists")
    with closing(sqlite3.connect(source)) as db, db:
        db.execute("CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        db.execute("CREATE TABLE imaginary_events(id INTEGER PRIMARY KEY, label TEXT NOT NULL)")
        for version in range(1, 7):
            db.execute("INSERT INTO schema_migrations VALUES (?,?)", (version, f"toy-{version}"))
        db.execute("INSERT INTO imaginary_events VALUES (1, 'sample fiction')")
    return source


def toy_guarded_audit(root: Path, source: Path) -> dict[str, object]:
    """Fixture-only attempt; no public interface accepts operator DB paths."""
    _ancestors_and_role(root, source)
    _sidecars(source)
    before = source.stat()
    original = _digest(source)
    with _windows_read_lease(source):
        _ancestors_and_role(root, source)
        _sidecars(source)
        head = header_info(source)
        # Do not equate user_version with Fabulaxiom's schema_migrations.
        if head["user_version"] != 0:
            raise ToySafetyStop("unexpected toy user_version")
        with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True, timeout=0)) as db:
            db.execute("PRAGMA query_only=ON")
            if db.execute("PRAGMA query_only").fetchone() != (1,):
                raise ToySafetyStop("query-only configuration failed")
            if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise ToySafetyStop("toy integrity failed")
            if db.execute("PRAGMA foreign_key_check").fetchall():
                raise ToySafetyStop("toy FK failure")
            rows = db.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall()
            if rows != [(1,), (2,), (3,), (4,), (5,), (6,)]:
                raise ToySafetyStop("wrong toy migration lineage")
            if db.execute("SELECT COUNT(*) FROM imaginary_events").fetchone() != (1,):
                raise ToySafetyStop("wrong toy event count")
        _sidecars(source)
        if original != _digest(source):
            raise ToySafetyStop("source byte change under read lease")
    after = source.stat()
    _sidecars(source)
    if original != _digest(source) or (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ToySafetyStop("source changed across toy audit")
    return {"status": "TOY_ONLY_PASS", "rollback_header": True,
            "schema_migrations": 6, "source_hash_unchanged": True}


def write_open_while_lease(source: Path) -> int:
    """Return Windows error code from an attempted WRITE open (toy fixture)."""
    if os.name != "nt":
        raise ToySafetyStop("Windows only")
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    f = kernel.CreateFileW
    f.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                  ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    f.restype = wintypes.HANDLE
    h = f(str(source), GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE,
          None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
    if h not in (None, ctypes.c_void_p(-1).value):
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle(h)
        raise ToySafetyStop("writer unexpectedly opened toy under read lease")
    return ctypes.get_last_error()


if __name__ == "__main__":
    import argparse
    cli = argparse.ArgumentParser(description="Synthetic Windows read-lease only")
    cli.add_argument("--self-test", action="store_true")
    opts = cli.parse_args()
    if not opts.self_test:
        cli.error("only --self-test; no operator source-path arguments")
    with tempfile.TemporaryDirectory(prefix=PREFIX) as folder:
        root = Path(folder)
        print(toy_guarded_audit(root, _toy_v6(root)))
