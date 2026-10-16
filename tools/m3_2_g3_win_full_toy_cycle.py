"""M3.2/G3/G4 TOY-ONLY: guarded Win32 source -> exclusive snapshot -> restore.

The CLI has ONLY --self-test. This module does not accept a user source/dest.
The toy source is SQLite-created inside TemporaryDirectory, and all output
is NEW in that same disposable temporary subtree. It is not safe for
production, active writers, untrusted ancestors, history or public backups.
"""
from __future__ import annotations

from contextlib import closing
import hashlib
import os
from pathlib import Path
import sqlite3
import tempfile

from m3_2_g3_win_pinned_toy_directory import inspect_under_pinned_toy_root
from m3_2_g3_win_single_handle_toy import (
    TOY_PREFIX, TOY_FILE, ToyGateError, create_fictional_toy,
    inspect_memory_image
)
from m3_2_g3_sealed_synthetic import (
    _exclusive_write_once, SyntheticGateBlocked
)

SNAPSHOT_DIR = "toy-new-custody"
RESTORE_DIR = "toy-third-restore"
SNAPSHOT_NAME = "snapshot.sqlite3"


class ToyCeremonyVeto(RuntimeError):
    pass


def _sha(image: bytes) -> str:
    return hashlib.sha256(image).hexdigest()


def _assert_root(root: Path) -> None:
    if root.parent != Path(tempfile.gettempdir()) or not root.name.startswith(TOY_PREFIX):
        raise ToyCeremonyVeto("only immediate private toy temp root allowed")
    if not root.is_dir() or root.is_symlink():
        raise ToyCeremonyVeto("toy temp root missing or symlinked")


def _new_dir(root: Path, role: str) -> Path:
    _assert_root(root)
    if role not in (SNAPSHOT_DIR, RESTORE_DIR):
        raise ToyCeremonyVeto("unrecognized toy output role")
    path = root / role
    if path.exists() or path.is_symlink():
        raise ToyCeremonyVeto("new-only toy destination collision")
    try:
        path.mkdir(mode=0o700, exist_ok=False)
    except FileExistsError as exc:
        raise ToyCeremonyVeto("destination directory collision") from exc
    if not path.is_dir() or path.is_symlink():
        raise ToyCeremonyVeto("new-only toy directory substitution")
    return path


def capture_toy(root: Path, *, version: int, test_hook=None, max_size: int = 2*1024*1024):
    """Physical source bytes from retained Win32 handle; SQL only RAM.

    No protected originals can be supplied: toy root + invented basename
    and fixture-owned source identity are mandatory.
    """
    _assert_root(root)
    source = root / TOY_FILE
    if not source.is_file() or source.is_symlink():
        raise ToyCeremonyVeto("expected invented source missing")
    if source.stat().st_size > max_size:
        raise ToyCeremonyVeto("toy source memory cap exceeded")
    before = source.read_bytes()
    evidence = inspect_under_pinned_toy_root(
        root, source, version=version, test_hook=test_hook, return_image=True
    )
    image = evidence.pop("image")
    if len(image) > max_size or not image or image != before:
        raise ToyCeremonyVeto("toy physical image / budget mismatch")
    if source.read_bytes() != before:
        raise ToyCeremonyVeto("toy source changed across capture")
    if evidence["source_digest"] != _sha(image):
        raise ToyCeremonyVeto("toy source digest mismatch")
    return image, evidence


def _write_new_snapshot(directory: Path, image: bytes):
    if directory.name not in (SNAPSHOT_DIR, RESTORE_DIR) or directory.is_symlink():
        raise ToyCeremonyVeto("unrecognized toy output directory")
    try:
        return _exclusive_write_once(directory / SNAPSHOT_NAME, image)
    except SyntheticGateBlocked as exc:
        raise ToyCeremonyVeto("exclusive toy file write refused") from exc


def _assert_copy(path: Path, image: bytes, version: int) -> None:
    if not path.is_file() or path.is_symlink():
        raise ToyCeremonyVeto("toy output file absent or reparse")
    read = path.read_bytes()
    if read != image or _sha(read) != _sha(image):
        raise ToyCeremonyVeto("toy output content/hash mismatch")
    inspect_memory_image(read, version)


def restore_toy(root: Path, expected: bytes, version: int) -> dict:
    """Restores ONLY a self-generated disposable snapshot to NEW third root."""
    _assert_root(root)
    src = root / SNAPSHOT_DIR / SNAPSHOT_NAME
    if src.is_symlink() or not src.is_file():
        raise ToyCeremonyVeto("toy captured snapshot missing")
    candidate = src.read_bytes()
    if candidate != expected:
        raise ToyCeremonyVeto("toy snapshot image mutated")
    inspect_memory_image(candidate, version)
    third = _new_dir(root, RESTORE_DIR)
    report = _write_new_snapshot(third, candidate)
    _assert_copy(third / SNAPSHOT_NAME, candidate, version)
    return report


def full_toy_cycle(root: Path, version: int) -> dict:
    _assert_root(root)
    source = root / TOY_FILE
    if source.exists() or source.is_symlink():
        raise ToyCeremonyVeto("toy source collision")
    created = create_fictional_toy(root, version)
    before = created.read_bytes()
    image, evidence = capture_toy(root, version=version)
    destination = _new_dir(root, SNAPSHOT_DIR)
    snapshot = _write_new_snapshot(destination, image)
    _assert_copy(destination / SNAPSHOT_NAME, image, version)
    restored = restore_toy(root, image, version)
    if created.read_bytes() != before:
        raise ToyCeremonyVeto("toy source modified")
    if snapshot["sha256"] != restored["sha256"] or snapshot["sha256"] != _sha(image):
        raise ToyCeremonyVeto("toy capture/restore digest mismatch")
    return {
        "scope": "FICTIONAL_TOY_ONLY",
        "version": version,
        "snapshot_sha256": snapshot["sha256"],
        "restore_sha256": restored["sha256"],
        "source_file_id_observed": evidence["source_identity"],
        "directory_file_id_observed": evidence["directory_identity"],
        "snapshot_bytes": len(image),
        "real_g3_authorized": False,
        "transient_ancestor_swap_resistance": "UNPROVEN",
    }


def self_test() -> None:
    if os.name != "nt":
        raise ToyCeremonyVeto("Win32 only")
    for version in (6, 7):
        with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as location:
            result = full_toy_cycle(Path(location), version)
            if result["real_g3_authorized"] or result["snapshot_sha256"] != result["restore_sha256"]:
                raise ToyCeremonyVeto("toy-only gate violated")
            print(f"FICTITIOUS_V{version}: G3/G4 toy-only qualified")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Win32 G3/G4 fictional toy full lifecycle only")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("ONLY --self-test, no operator file paths")
    self_test()
