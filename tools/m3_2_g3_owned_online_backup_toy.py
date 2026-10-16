"""M3.2 G3: EXISTING toy SQLite owner -> RAM Online Backup -> sealed toy restore.

Laboratory only. The source connection is opened by invented_toy_owner()
inside an internally created TemporaryDirectory BEFORE capture_toy_owner().
Capture never connects to the source pathname or runs production migrations.
No CLI accepts source/destination paths, credentials or operator data.
This cannot establish real source custody or grant actual G3 permission.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import sqlite3
import tempfile

from m3_2_g3_win_single_handle_toy import (
    TOY_PREFIX, TOY_FILE, ToyGateError, create_fictional_toy,
    inspect_memory_image,
)
from m3_2_g3_win_full_toy_cycle import (
    SNAPSHOT_DIR, RESTORE_DIR, SNAPSHOT_NAME,
    ToyCeremonyVeto, _new_dir, _write_new_snapshot, _assert_copy, restore_toy,
)

_MAX_TOY_IMAGE = 2 * 1024 * 1024
_TOY_ISSUER = object()


class OwnedToyVeto(RuntimeError):
    """A toy-only, fail-closed refusal; not a real custody status."""


@dataclass(frozen=True)
class OwnedToy:
    root: Path
    source: Path
    connection: sqlite3.Connection
    version: int
    issuer: object


@contextmanager
def invented_toy_owner(version: int):
    """Create/close invented SQLite and yield a pre-OPENED owner connection."""
    if version not in (6, 7):
        raise OwnedToyVeto("fictional version not supported")
    with tempfile.TemporaryDirectory(prefix=TOY_PREFIX) as name:
        root = Path(name)
        source = create_fictional_toy(root, version)
        # Sole intended source open here, BEFORE backup_owner_to_ram is called.
        with closing(sqlite3.connect(source)) as connection:
            yield OwnedToy(root, source, connection, version, _TOY_ISSUER)


def _verify_owned_toy(owner: OwnedToy, max_bytes: int) -> None:
    if not isinstance(owner, OwnedToy) or owner.issuer is not _TOY_ISSUER:
        raise OwnedToyVeto("not a fixture-issued owner")
    if owner.version not in (6, 7) or owner.source.name != TOY_FILE:
        raise OwnedToyVeto("invented SQLite role invalid")
    if not (0 < max_bytes <= _MAX_TOY_IMAGE):
        raise OwnedToyVeto("toy image memory budget invalid")
    if owner.root.parent != Path(tempfile.gettempdir()) or not owner.root.name.startswith(TOY_PREFIX):
        raise OwnedToyVeto("not an immediate temporary toy root")
    if owner.root.is_symlink() or not owner.root.is_dir():
        raise OwnedToyVeto("toy root invalid")
    if owner.source != owner.root / TOY_FILE or owner.source.is_symlink() or not owner.source.is_file():
        raise OwnedToyVeto("toy source role invalid")
    try:
        if owner.connection.in_transaction:
            raise OwnedToyVeto("owner has an uncommitted source transaction")
        attached = owner.connection.execute("PRAGMA database_list").fetchall()
        if len(attached) != 1 or attached[0][1] != "main":
            raise OwnedToyVeto("unqualified toy attached databases")
        path = attached[0][2]
        if not path or os.path.normcase(os.path.abspath(path)) != os.path.normcase(os.path.abspath(owner.source)):
            raise OwnedToyVeto("existing owner connection bound to a different source")
        pages = int(owner.connection.execute("PRAGMA page_count").fetchone()[0])
        page_size = int(owner.connection.execute("PRAGMA page_size").fetchone()[0])
    except sqlite3.Error as exc:
        raise OwnedToyVeto("existing toy owner connection unavailable") from exc
    if pages <= 0 or page_size <= 0 or pages * page_size > max_bytes:
        raise OwnedToyVeto("toy source exceeds memory budget")


def backup_owner_to_ram(owner: OwnedToy, *, max_bytes: int = _MAX_TOY_IMAGE) -> tuple[bytes, dict]:
    """Use caller's PRE-EXISTING connection; only new sqlite3.connect is :memory:."""
    _verify_owned_toy(owner, max_bytes)
    source_changes = owner.connection.total_changes
    try:
        if not hasattr(sqlite3.Connection, "serialize") or not hasattr(sqlite3.Connection, "deserialize"):
            raise OwnedToyVeto("SQLite RAM serialize/deserialize unavailable")
        with closing(sqlite3.connect(":memory:")) as ram:
            owner.connection.backup(ram, pages=-1, name="main", sleep=0.0)
            if ram.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise OwnedToyVeto("RAM backup integrity failure")
            if ram.execute("PRAGMA foreign_key_check").fetchall():
                raise OwnedToyVeto("RAM backup foreign-key violation")
            lineage = ram.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall()
            if lineage != [(i,) for i in range(1, owner.version + 1)]:
                raise OwnedToyVeto("RAM backup schema_migrations mismatch")
            if ram.execute("SELECT COUNT(*) FROM imagined_books").fetchone()[0] != 1:
                raise OwnedToyVeto("RAM backup toy books count mismatch")
            if ram.execute("SELECT COUNT(*) FROM invented_facts").fetchone()[0] != 1:
                raise OwnedToyVeto("RAM backup toy facts count mismatch")

            before = ram.serialize()
            normalized = before[18:20] == b"\x02\x02"
            if normalized:
                # WAL snapshot in RAM sometimes serializes with a WAL header,
                # which cannot be used as a standalone file without WAL state.
                # VACUUM affects ONLY the RAM destination, never the source.
                ram.execute("VACUUM")
                if ram.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                    raise OwnedToyVeto("normalized RAM integrity failure")
            image = ram.serialize()
            if len(image) > max_bytes:
                raise OwnedToyVeto("RAM image exceeds toy memory budget")
    except sqlite3.Error as exc:
        raise OwnedToyVeto("transactional toy backup/validation failed") from exc
    # inspect_memory_image deserializes the captured image into ANOTHER RAM
    # connection and confirms rollback-format header, schema & toy FK state.
    try:
        inspect_memory_image(image, owner.version)
        _verify_owned_toy(owner, max_bytes)
    except ToyGateError as exc:
        raise OwnedToyVeto("serialized image is not a stand-alone toy SQLite") from exc
    if owner.connection.total_changes != source_changes:
        raise OwnedToyVeto("source owner changed during capture")
    return image, {
        "scope": "INVENTED_OWNER_TOY_ONLY",
        "strategy": "ONLINE_BACKUP_EXISTING_OWNER_TO_RAM",
        "bytes": len(image),
        "sha256": hashlib.sha256(image).hexdigest(),
        "ram_vacuum_normalized_wal_header": normalized,
        "source_connection_reopened": False,
        "real_g3_authorized": False,
        "real_source_provenance": "UNPROVEN",
    }


def sealed_owned_toy_cycle(owner: OwnedToy, *, max_bytes: int = _MAX_TOY_IMAGE) -> dict:
    """New-only fixture G3 target and fresh third-location toy G4 restore."""
    image, audit = backup_owner_to_ram(owner, max_bytes=max_bytes)
    output = _new_dir(owner.root, SNAPSHOT_DIR)
    written = _write_new_snapshot(output, image)
    _assert_copy(output / SNAPSHOT_NAME, image, owner.version)
    restored = restore_toy(owner.root, image, owner.version)
    if audit["sha256"] != written["sha256"] or written["sha256"] != restored["sha256"]:
        raise OwnedToyVeto("new-only toy backup/restore digest differs")
    return dict(audit, third_location_restored=True, snapshot_sha256=written["sha256"])


def self_test() -> None:
    for version in (6, 7):
        with invented_toy_owner(version) as owner:
            result = sealed_owned_toy_cycle(owner)
            if result["real_g3_authorized"] or not result["third_location_restored"]:
                raise OwnedToyVeto("real G3 must remain blocked")
            print(f"EXISTING_OWNER_V{version}: TOY_G3_G4_PASS")
    print("REAL_G3: NOT_AUTHORIZED")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Existing-owner SQLite backup, toy only")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("ONLY --self-test; no original source or output paths")
    self_test()
