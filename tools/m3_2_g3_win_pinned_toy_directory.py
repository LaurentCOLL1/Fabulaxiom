"""Win32 retained toy-directory handle identity experiment. NO operator paths.

All files are invented under TemporaryDirectory. Holding a directory
handle without FILE_SHARE_DELETE does not guarantee directory rename denial.
This tests observable mismatches, not every intermediate namespace swap.
It is not a general anti-race guarantee for parent ancestors or real custody.
"""
from __future__ import annotations

from contextlib import contextmanager
import ctypes
from ctypes import wintypes
import os
from pathlib import Path
import stat
import tempfile

from m3_2_g3_win_single_handle_toy import (
    TOY_PREFIX, TOY_FILE, ToyGateError, _toy_path, _no_sidecars,
    _locked_read_handle, _read_full_image, _get_file_info,
    _identity, _kernel, inspect_memory_image, create_fictional_toy,
)

BACKUP_SEMANTICS = 0x02000000
OPEN_REPARSE = 0x00200000
OPEN_EXISTING = 3
READ_ATTRIBUTES = 0x00000080
SHARE_READ = 0x00000001
SHARE_WRITE = 0x00000002
DIRECTORY_ATTR = 0x00000010
REPARSE_ATTR = 0x00000400


def _toy_root(root: Path, source: Path) -> None:
    _toy_path(root, source)
    if root.parent != Path(tempfile.gettempdir()):
        raise ToyGateError("toy parent not the runtime temp directory")
    for value in (root.parent, root, source):
        info = value.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & REPARSE_ATTR:
            raise ToyGateError("toy path/parent reparse point detected")


@contextmanager
def pinned_toy_directory(root: Path):
    """Pin the fixture directory itself, no DELETE sharing. No privilege elevation."""
    if os.name != "nt":
        raise ToyGateError("Windows only")
    if root.parent != Path(tempfile.gettempdir()) or not root.name.startswith(TOY_PREFIX):
        raise ToyGateError("not a toy directory")
    if root.is_symlink() or not root.is_dir():
        raise ToyGateError("toy directory missing/reparse")
    kernel = _kernel()
    create = kernel.CreateFileW
    create.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE
    ]
    create.restype = wintypes.HANDLE
    h = create(str(root), READ_ATTRIBUTES, SHARE_READ | SHARE_WRITE,
               None, OPEN_EXISTING, BACKUP_SEMANTICS | OPEN_REPARSE, None)
    if h in (None, ctypes.c_void_p(-1).value):
        raise ToyGateError(f"directory handle refused: {ctypes.get_last_error()}")
    close = kernel.CloseHandle
    close.argtypes = [wintypes.HANDLE]
    close.restype = wintypes.BOOL
    try:
        info = _get_file_info(kernel, h)
        if not (int(info.dwFileAttributes) & DIRECTORY_ATTR) or (
            int(info.dwFileAttributes) & REPARSE_ATTR
        ):
            raise ToyGateError("directory handle identity/type invalid")
        yield kernel, h, _identity(info)
    finally:
        if not close(h):
            raise ToyGateError("directory handle close failed")


def _toy_directory_path_identity(root: Path):
    """Reopen *toy directory only* to detect path-to-handle mismatch."""
    with pinned_toy_directory(root) as (_, __, identity):
        return identity


def inspect_under_pinned_toy_root(root: Path, source: Path, *, version: int, test_hook=None):
    """Verify single source HANDLE while pinned toy root is held; RAM SQLite only."""
    _toy_root(root, source)
    _no_sidecars(source)
    with pinned_toy_directory(root) as (kroot, hroot, root_identity):
        if _toy_directory_path_identity(root) != root_identity:
            raise ToyGateError("toy directory pathname mismatch before read")
        with _locked_read_handle(source) as (ksrc, hsrc):
            _toy_root(root, source)
            _no_sidecars(source)
            if test_hook is not None:
                test_hook(root, source)  # Only callable by synthetic tests.
            image, source_identity = _read_full_image(ksrc, hsrc, max_bytes=2*1024*1024)
            evidence = inspect_memory_image(image, version)
            _no_sidecars(source)
            if _identity(_get_file_info(ksrc, hsrc)) != source_identity:
                raise ToyGateError("toy source handle changed")
            if _identity(_get_file_info(kroot, hroot)) != root_identity:
                raise ToyGateError("toy directory handle changed")
            if _toy_directory_path_identity(root) != root_identity:
                raise ToyGateError("toy directory pathname mismatch after read")
            _toy_root(root, source)
    return {"status": "TOY_ONLY_PASS", "directory_identity": True,
            "source_identity": True, "source_digest": evidence["sha256"],
            "version": version}


def self_test() -> None:
    for version in (6, 7):
        with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as name:
            root = Path(name)
            src = create_fictional_toy(root, version)
            before = src.read_bytes()
            result = inspect_under_pinned_toy_root(root, src, version=version)
            if src.read_bytes() != before or result["version"] != version:
                raise ToyGateError("toy source changed")
    print("G3 PINNED TOY DIRECTORY: PASS (NO OPERATOR DATA)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Win32 toy directory-handle experiment only")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("only --self-test; no operator paths allowed")
    self_test()
