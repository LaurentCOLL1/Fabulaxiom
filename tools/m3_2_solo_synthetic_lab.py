"""M3.2 prospective-baseline SYNTHETIC-ONLY laboratory.

NO OPERATOR FILE SUPPORT. Do not use for production or preserved SQLite databases.
The distinct-source WAL open, exclusive-destination filesystem and signed-manifest
guarantees for the future Windows ceremony are NOT implemented by this fixture.

This tool has no generic --source / --destination arguments. Import in tests only.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
from urllib.parse import quote


class GateBlocked(RuntimeError):
    """A mandatory evidence or safety gate was not met."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def new_reserved_file(folder: Path, basename: str) -> Path:
    """Atomic creation against an existing name (lab only; not production proof).

    SQLITE may open a new handle after this function: WITHOUT a separately
    secured parent directory this does not defeat every Windows TOCTOU attack.
    """
    if folder.is_symlink() or not folder.is_dir():
        raise GateBlocked("unsafe output directory")
    if basename not in {"snapshot.sqlite", "restore.sqlite"}:
        raise GateBlocked("output name not authorized by synthetic fixture")
    target = folder / basename
    try:
        descriptor = os.open(target, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
    except FileExistsError as exc:
        raise GateBlocked("destination already exists") from exc
    else:
        os.close(descriptor)
    return target


def new_synthetic_source(folder: Path, *, version: int = 6) -> Path:
    """Construct a freshly isolated fictitious database, never an operator DB."""
    if version not in (6, 7):
        raise GateBlocked("unsupported schema version")
    if not folder.is_dir() or folder.is_symlink():
        raise GateBlocked("source folder not private fixture")
    source = folder / "synthetic_source.sqlite"
    if source.exists() or source.is_symlink():
        raise GateBlocked("fixture source exists")
    with closing(sqlite3.connect(source)) as conn, conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.executescript("""
            CREATE TABLE universes (
                universe_id TEXT PRIMARY KEY,
                title TEXT NOT NULL
            ) STRICT;
            CREATE TABLE scene_text_revisions (
                revision_id TEXT PRIMARY KEY,
                universe_id TEXT NOT NULL REFERENCES universes(universe_id),
                previous_revision_id TEXT REFERENCES scene_text_revisions(revision_id),
                body TEXT NOT NULL
            ) STRICT;
            CREATE TABLE narrative_facts (
                fact_id TEXT PRIMARY KEY,
                universe_id TEXT NOT NULL REFERENCES universes(universe_id),
                statement TEXT NOT NULL
            ) STRICT;
        """)
        if version == 7:
            conn.executescript("""
                CREATE TABLE world_time_anchors (
                    anchor_id TEXT PRIMARY KEY,
                    universe_id TEXT NOT NULL REFERENCES universes(universe_id),
                    label TEXT NOT NULL
                ) STRICT;
            """)
        conn.execute("INSERT INTO universes VALUES (?,?)", ("w-1", "Monde fictif"))
        conn.execute("INSERT INTO scene_text_revisions VALUES (?,?,?,?)",
                     ("r-1", "w-1", None, "Texte 🌍 original"))
        conn.execute("INSERT INTO scene_text_revisions VALUES (?,?,?,?)",
                     ("r-2", "w-1", "r-1", "Révision ultérieure"))
        conn.execute("INSERT INTO narrative_facts VALUES (?,?,?)",
                     ("f-1", "w-1", "fait documenté"))
        if version == 7:
            conn.execute("INSERT INTO world_time_anchors VALUES (?,?,?)",
                         ("a-1", "w-1", "avant le chapitre"))
        conn.execute(f"PRAGMA user_version={version}")
    return source


def logical_digest(conn: sqlite3.Connection) -> tuple[str, dict[str, int]]:
    """Canonical JSON digest with explicit schema, table order, row order.

    For the controlled synthetic fixture only; not a stable production
    canonicalization specification for arbitrary SQLite BLOB/REAL/tables.
    """
    meta = conn.execute(
        "SELECT name, sql FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    if not meta:
        raise GateBlocked("empty schema")
    canonical = []
    counts = {}
    for name, ddl in meta:
        if name not in {"universes", "scene_text_revisions", "narrative_facts", "world_time_anchors"}:
            raise GateBlocked("unexpected table")
        columns = [str(col[1]) for col in conn.execute(f'PRAGMA table_info("{name}")')]
        rows = conn.execute(f'SELECT * FROM "{name}" ORDER BY rowid').fetchall()
        counts[name] = len(rows)
        canonical.append({"table": name, "ddl": ddl, "columns": columns, "rows": rows})
    payload = json.dumps(canonical, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest(), counts


def independent_count_oracle(conn: sqlite3.Connection) -> dict[str, int]:
    """Second SQL enumeration method; still shares SQLite engine, not a reviewer."""
    result = {}
    names = sorted(row[0] for row in conn.execute(
        "SELECT name FROM pragma_table_list WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ))
    for name in names:
        if name not in {"universes", "scene_text_revisions", "narrative_facts", "world_time_anchors"}:
            raise GateBlocked("unexpected table in oracle")
        result[name] = conn.execute(f'SELECT count(*) FROM "{name}"').fetchone()[0]
    return result


def validate_new_copy(path: Path, *, schema: int, expected_digest: str | None = None,
                      expected_sha256: str | None = None,
                      expected_counts: dict[str, int] | None = None) -> dict:
    if schema not in (6, 7):
        raise GateBlocked("unsupported version")
    if not path.is_file() or path.is_symlink():
        raise GateBlocked("copy missing or symlink")
    observed_hash = sha256(path)
    if expected_sha256 is not None and observed_hash != expected_sha256:
        raise GateBlocked("SHA-256 mismatch")
    try:
        # This read-only connection is ONLY to a disposable synthetic copy.
        # mode=ro is not guaranteed no-sidecar for protected originals.
        uri = path.resolve().as_uri() + "?mode=ro"
        with closing(sqlite3.connect(uri, uri=True)) as conn:
            check = conn.execute("PRAGMA integrity_check").fetchall()
            if check != [("ok",)]:
                raise GateBlocked("integrity_check failed")
            if conn.execute("PRAGMA foreign_key_check").fetchall():
                raise GateBlocked("foreign key failure")
            user_version = conn.execute("PRAGMA user_version").fetchone()[0]
            if user_version != schema:
                raise GateBlocked("unexpected schema version")
            digest, counts = logical_digest(conn)
            if counts != independent_count_oracle(conn):
                raise GateBlocked("contradictory table counts")
            if counts.get("universes") != 1 or counts.get("scene_text_revisions") != 2:
                raise GateBlocked("revision ancestry/count altered")
            if counts.get("narrative_facts") != 1:
                raise GateBlocked("facts altered")
            if schema == 7 and counts.get("world_time_anchors") != 1:
                raise GateBlocked("v7 anchor absent")
            if schema == 6 and "world_time_anchors" in counts:
                raise GateBlocked("v7 table in v6")
            relations = dict(conn.execute(
                "SELECT revision_id, previous_revision_id FROM scene_text_revisions"
            ).fetchall())
            if relations != {"r-1": None, "r-2": "r-1"}:
                raise GateBlocked("revision lineage altered")
            if expected_counts is not None and counts != expected_counts:
                raise GateBlocked("count manifest mismatch")
            if expected_digest is not None and digest != expected_digest:
                raise GateBlocked("logical digest mismatch")
    except sqlite3.DatabaseError as exc:
        raise GateBlocked("invalid SQLite copy") from exc
    return {"sha256": observed_hash, "digest": digest, "schema": schema,
            "counts": counts, "synthetic_only": True}


def backup_synthetic(source: Path, output_directory: Path) -> tuple[Path, dict]:
    """Only for test-created DB and a fresh owned temporary output directory."""
    output = new_reserved_file(output_directory, "snapshot.sqlite")
    try:
        with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(output)) as target:
            src.backup(target, pages=8, sleep=0.01)
        with closing(sqlite3.connect(source)) as source_check:
            schema = source_check.execute("PRAGMA user_version").fetchone()[0]
        return output, validate_new_copy(output, schema=schema)
    except Exception:
        # We intentionally leave a newly-created failed output to inspect.
        raise


def restore_synthetic(snapshot: Path, output_directory: Path, manifest: dict) -> tuple[Path, dict]:
    """Run restoration only on fresh synthetic destination, not app marker."""
    validate_new_copy(snapshot, schema=manifest["schema"],
                      expected_sha256=manifest["sha256"],
                      expected_digest=manifest["digest"], expected_counts=manifest["counts"])
    output = new_reserved_file(output_directory, "restore.sqlite")
    with closing(sqlite3.connect(snapshot)) as src, closing(sqlite3.connect(output)) as dst:
        src.backup(dst, pages=8, sleep=0.01)
    result = validate_new_copy(output, schema=manifest["schema"],
                               expected_digest=manifest["digest"],
                               expected_counts=manifest["counts"])
    return output, result


def selftest() -> None:
    with tempfile.TemporaryDirectory(prefix="fabulaxiom-m32-synthetic-") as root:
        root_dir = Path(root)
        for version in (6, 7):
            source_dir = root_dir / f"src_{version}"
            output_dir = root_dir / f"out_{version}"
            restored_dir = root_dir / f"restore_{version}"
            for d in (source_dir, output_dir, restored_dir):
                d.mkdir(mode=0o700)
            src = new_synthetic_source(source_dir, version=version)
            source_digest = sha256(src)
            snap, manifest = backup_synthetic(src, output_dir)
            restored, evidence = restore_synthetic(snap, restored_dir, manifest)
            if evidence["digest"] != manifest["digest"] or source_digest != sha256(src):
                raise GateBlocked("synthetic source changed / restore mismatch")
            if restored.samefile(src):
                raise GateBlocked("restored original in place")
    print("M3.2 SOLO SYNTHETIC SELFTEST: PASS (NO OPERATOR PATHS)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic-only M3.2 qualification")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("Only --self-test supported. No operator --source or --destination.")
    selftest()


if __name__ == "__main__":
    main()
