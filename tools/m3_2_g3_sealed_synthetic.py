"""G3 SEALED *SYNTHETIC ONLY* SQLite experiment. NO operator-path CLI.

Makes its own toy v6/v7 schemas under TemporaryDirectory. SQLite source
opening and real Windows ACL/reparse/custody controls are not qualified.
Unlike a conventional backup-to-file, target data are written with the same
exclusive fd returned by os.open(O_CREAT|O_EXCL) and never reopened for write.
"""
from __future__ import annotations

from contextlib import closing
import hashlib
import os
from pathlib import Path
import sqlite3
import tempfile


class SyntheticGateBlocked(RuntimeError):
    pass


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _make_synthetic_db(parent: Path, version: int) -> Path:
    if version not in (6, 7):
        raise SyntheticGateBlocked("unsupported toy schema")
    source = parent / f"toy-{version}.sqlite3"
    if source.exists() or source.is_symlink():
        raise SyntheticGateBlocked("toy fixture exists")
    # Disposable toy DB only; NOT a reproduction of Fabulaxiom's real schema.
    with closing(sqlite3.connect(source)) as db, db:
        db.execute("CREATE TABLE invented_events (id INTEGER PRIMARY KEY, word TEXT NOT NULL)")
        db.execute("INSERT INTO invented_events VALUES (1, 'fictional world')")
        db.execute("CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        for i in range(1, version + 1):
            db.execute("INSERT INTO schema_migrations VALUES (?, ?)", (i, f"fixture-{i:03}"))
    return source


def _snapshot_toy_to_bytes(source: Path, *, limit: int = 1024 * 1024) -> bytes:
    if source.name not in ("toy-6.sqlite3", "toy-7.sqlite3"):
        raise SyntheticGateBlocked("not a permitted toy name")
    if limit <= 0:
        raise SyntheticGateBlocked("memory limit invalid")
    # Read-only SQLite source: ALLOWED FOR DISPOSABLE FIXTURES ONLY.
    with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as src:
        with closing(sqlite3.connect(":memory:")) as ram:
            src.backup(ram, pages=-1)
            if ram.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise SyntheticGateBlocked("toy RAM integrity failed")
            if ram.execute("PRAGMA foreign_key_check").fetchall():
                raise SyntheticGateBlocked("toy RAM foreign key violation")
            page_count = ram.execute("PRAGMA page_count").fetchone()[0]
            page_size = ram.execute("PRAGMA page_size").fetchone()[0]
            if page_count * page_size > limit:
                raise SyntheticGateBlocked("memory budget exceeded")
            image = ram.serialize()
    if len(image) > limit:
        raise SyntheticGateBlocked("memory budget exceeded")
    return image


def _exclusive_write_once(target: Path, payload: bytes) -> dict:
    """One write-capable handle from exclusive create through flush/fsync.

    This demonstration DOES NOT establish production Win32 parent-directory
    anti-reparse or ACL guarantees, malicious same-user race resistance, or
    safe source opening. No production source/dest CLI is provided.
    """
    if target.name != "snapshot.sqlite3" or target.parent.is_symlink() or not target.parent.is_dir():
        raise SyntheticGateBlocked("unapproved toy destination")
    if not payload.startswith(b"SQLite format 3\x00"):
        raise SyntheticGateBlocked("invalid image header")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(target, flags, 0o600)
    except FileExistsError as exc:
        raise SyntheticGateBlocked("destination collision, untouched") from exc
    with os.fdopen(fd, "wb") as output:
        output.write(payload)
        output.flush()
        os.fsync(output.fileno())
    before = target.stat(follow_symlinks=False)
    if target.is_symlink() or before.st_size != len(payload):
        raise SyntheticGateBlocked("target size/identity changed")
    observed = target.read_bytes()
    after = target.stat(follow_symlinks=False)
    if (after.st_dev, after.st_ino, after.st_size) != (before.st_dev, before.st_ino, before.st_size):
        raise SyntheticGateBlocked("target identity changed")
    if _hash(observed) != _hash(payload):
        raise SyntheticGateBlocked("payload mismatch")
    return {"sha256": _hash(payload), "bytes": len(payload), "synthetic_only": True}


def synthetic_trial(version: int = 6) -> dict:
    if version not in (6, 7):
        raise SyntheticGateBlocked("unsupported synthetic version")
    with tempfile.TemporaryDirectory(prefix="fabulaxiom-m32-g3-toy-") as root:
        parent = Path(root)
        source = _make_synthetic_db(parent, version)
        source_hash = _hash(source.read_bytes())
        destination = parent / "brand_new_destination"
        destination.mkdir(mode=0o700, exist_ok=False)
        image = _snapshot_toy_to_bytes(source)
        report = _exclusive_write_once(destination / "snapshot.sqlite3", image)
        if _hash(source.read_bytes()) != source_hash:
            raise SyntheticGateBlocked("toy source changed")
        # Verification uses only the newly generated disposable image.
        with closing(sqlite3.connect((destination / "snapshot.sqlite3").resolve().as_uri() + "?mode=ro", uri=True)) as db:
            actual = db.execute("SELECT MAX(version) FROM schema_migrations").fetchone()[0]
            if actual != version:
                raise SyntheticGateBlocked("toy version mismatch")
            if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise SyntheticGateBlocked("toy persisted integrity failed")
        return report


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="G3 synthetic sealed snapshot only")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("Only --self-test: cannot specify operator source or destination")
    for version in (6, 7):
        value = synthetic_trial(version)
        print(f"G3_V{version} TOY_ONLY=PASS bytes={value['bytes']}")


if __name__ == "__main__":
    main()
