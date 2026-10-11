"""M3.1 final independent read-only v7 third-copy and time-constraint audit.

Never opens protected SQLite files in write mode. Negative/positive DML
exercises run only against a private SQLite ':memory:' copy. No on-disk
migration, manifest, test data or production pointer is created or changed.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import sys
from uuid import uuid4

import m3_1_v6_audit as audit
import m3_1_v6_backup as backup
import m3_1_v7_copy_rehearsal as v7


class FinalAuditStop(Exception):
    pass


def _third_folder(root: Path, relative: str) -> Path:
    path = Path(relative.replace("\\", "/"))
    if (len(path.parts) != 3 or path.parts[:2] !=
            ("operator-qualification", "m3_1") or
            not re.fullmatch(
                r"v7_copy_rehearsal_[0-9]{8}T[0-9]{6}Z-[0-9a-f]{32}",
                path.parts[2],
            )):
        raise FinalAuditStop("unapproved_third_copy_path")
    directory = root
    for part in path.parts:
        directory = directory / part
        audit._directory(directory)
    return directory


def _denied(db: sqlite3.Connection, sql: str, args: tuple,
            reason: str | None = None) -> None:
    try:
        db.execute(sql, args)
    except sqlite3.IntegrityError as exc:
        if reason is not None and reason not in str(exc):
            raise FinalAuditStop("unexpected_constraint_reason") from exc
    else:
        raise FinalAuditStop("constraint_unexpectedly_accepted")


def _exercise_time_constraints(third: Path) -> int:
    """All writes are to RAM, not to third/protected file."""
    with closing(sqlite3.connect(
        third.as_uri() + "?mode=ro", uri=True, timeout=0
    )) as read_only:
        read_only.execute("PRAGMA query_only=ON")
        with closing(sqlite3.connect(":memory:")) as mem:
            read_only.backup(mem)
            mem.execute("PRAGMA foreign_keys=ON")
            if mem.execute("PRAGMA foreign_keys").fetchone() != (1,):
                raise FinalAuditStop("memory_foreign_keys_off")
            if mem.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise FinalAuditStop("memory_clone_integrity")
            historic = mem.execute(
                "SELECT n.universe_id,r.id FROM scene_text_revisions r "
                "JOIN scenes s ON r.scene_id=s.id "
                "JOIN chapters c ON s.chapter_id=c.id "
                "JOIN novels n ON c.novel_id=n.id "
                "ORDER BY r.id LIMIT 1"
            ).fetchone()
            if historic is None:
                raise FinalAuditStop("historical_revision_for_scope_missing")
            universe_a, revision_a = historic
            prefix = "m31_ram_" + uuid4().hex + "_"
            universe_b = prefix + "universe_b"
            calendar_a = prefix + "cal_a"
            calendar_b = prefix + "cal_b"
            event_a = prefix + "event_a"
            event_b = prefix + "event_b"
            character_a = prefix + "character"
            a, b, c = (prefix + suffix for suffix in ("a", "b", "c"))
            other_anchor = prefix + "other_anchor"

            mem.execute("INSERT INTO universes(id,name) VALUES(?,?)",
                        (universe_b, "Disposable memory universe"))
            for ident, universe, kind in (
                (event_a, universe_a, "event"),
                (event_b, universe_b, "event"),
                (character_a, universe_a, "character"),
            ):
                mem.execute(
                    "INSERT INTO narrative_entities(id,universe_id,kind,name)"
                    " VALUES(?,?,?,?)",
                    (ident, universe, kind, "Memory-only fixture")
                )
            for ident, universe in (
                (calendar_a, universe_a), (calendar_b, universe_b)
            ):
                mem.execute(
                    "INSERT INTO fictional_calendars"
                    "(id,universe_id,name,definition_text) VALUES(?,?,?,?)",
                    (ident, universe, "Fictional clock", "Days from the first moon")
                )
            tests = 0

            def case(fn):
                nonlocal tests
                mem.execute("SAVEPOINT audit_scenario")
                try:
                    fn()
                    if mem.execute("PRAGMA foreign_key_check").fetchone():
                        raise FinalAuditStop("memory_scenario_foreign_keys")
                    tests += 1
                finally:
                    mem.execute("ROLLBACK TO audit_scenario")
                    mem.execute("RELEASE audit_scenario")

            def anchor(ident, universe, kind="unknown", calendar=None,
                       event=None, revision=None, exact=None, start=None,
                       end=None, precision=None):
                mem.execute(
                    "INSERT INTO world_time_anchors"
                    "(id,universe_id,time_kind,calendar_id,event_entity_id,"
                    "source_revision_id,exact_label,window_start_text,"
                    "window_end_text,precision_text)"
                    " VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (ident, universe, kind, calendar, event, revision,
                     exact, start, end, precision)
                )

            def exact_valid():
                anchor(a, universe_a, kind="exact", calendar=calendar_a,
                       event=event_a, revision=revision_a,
                       exact="Year 4 / white-moon", precision="moon-cycle")
                value = mem.execute(
                    "SELECT exact_label FROM world_time_anchors WHERE id=?",
                    (a,)
                ).fetchone()
                if value != ("Year 4 / white-moon",):
                    raise FinalAuditStop("fictional_raw_calendar_changed")
            case(exact_valid)
            case(lambda: anchor(a, universe_a, kind="unknown"))
            case(lambda: anchor(
                a, universe_a, kind="approximate", calendar=calendar_a,
                start="before dawn", end="last storm", precision="season"
            ))
            case(lambda: _denied(
                mem, "INSERT INTO world_time_anchors"
                "(id,universe_id,time_kind,exact_label) VALUES(?,?,'exact',?)",
                (a, universe_a, "no calendar")
            ))
            case(lambda: _denied(
                mem, "INSERT INTO world_time_anchors"
                "(id,universe_id,time_kind,calendar_id,window_start_text)"
                " VALUES(?,?,'approximate',?,?)",
                (a, universe_a, calendar_a, "fuzzy start")
            ))
            case(lambda: _denied(
                mem, "INSERT INTO world_time_anchors"
                "(id,universe_id,time_kind,calendar_id,exact_label)"
                " VALUES(?,?,'unknown',?,?)",
                (a, universe_a, calendar_a, "not unknown")
            ))
            case(lambda: _denied(
                mem, "INSERT INTO world_time_anchors"
                "(id,universe_id,time_kind,calendar_id,exact_label)"
                " VALUES(?,?,'exact',?,?)",
                (a, universe_a, calendar_b, "foreign calendar")
            ))

            def scoped_events():
                anchor(a, universe_a, event=event_a, revision=revision_a)
                _denied(
                    mem, "INSERT INTO world_time_anchors"
                    "(id,universe_id,time_kind,event_entity_id)"
                    " VALUES(?,?,'unknown',?)",
                    (b, universe_a, event_b)
                )
                _denied(
                    mem, "INSERT INTO world_time_anchors"
                    "(id,universe_id,time_kind,event_entity_id)"
                    " VALUES(?,?,'unknown',?)",
                    (b, universe_a, character_a),
                    "world time event ownership or type mismatch"
                )
                _denied(
                    mem, "INSERT INTO world_time_anchors"
                    "(id,universe_id,time_kind,source_revision_id)"
                    " VALUES(?,?,'unknown',?)",
                    (other_anchor, universe_b, revision_a),
                    "world time revision universe mismatch"
                )
            case(scoped_events)

            def precedence():
                for ident in (a, b, c):
                    anchor(ident, universe_a)
                for edge_id, before, after in (
                    (prefix+"ab", a, b), (prefix+"bc", b, c)
                ):
                    mem.execute(
                        "INSERT INTO world_time_precedences"
                        "(id,universe_id,before_anchor_id,after_anchor_id,reason)"
                        " VALUES(?,?,?,?,?)",
                        (edge_id, universe_a, before, after, "Declared by human")
                    )
                _denied(
                    mem, "INSERT INTO world_time_precedences"
                    "(id,universe_id,before_anchor_id,after_anchor_id,reason)"
                    " VALUES(?,?,?,?,?)",
                    (prefix+"ca", universe_a, c, a, "cycle"),
                    "world time precedence cycle"
                )
                _denied(
                    mem, "INSERT INTO world_time_precedences"
                    "(id,universe_id,before_anchor_id,after_anchor_id,reason)"
                    " VALUES(?,?,?,?,?)",
                    (prefix+"self", universe_a, a, a, "self")
                )
                anchor(other_anchor, universe_b)
                _denied(
                    mem, "INSERT INTO world_time_precedences"
                    "(id,universe_id,before_anchor_id,after_anchor_id,reason)"
                    " VALUES(?,?,?,?,?)",
                    (prefix+"cross", universe_a, a, other_anchor,
                     "not same universe")
                )
                _denied(
                    mem, "INSERT INTO world_time_precedences"
                    "(id,universe_id,before_anchor_id,after_anchor_id,reason)"
                    " VALUES(?,?,?,?,?)",
                    (prefix+"blank", universe_a, a, c, "  ")
                )
            case(precedence)

            def immutability():
                anchor(a, universe_a)
                anchor(b, universe_a)
                mem.execute(
                    "INSERT INTO world_time_precedences"
                    "(id,universe_id,before_anchor_id,after_anchor_id,reason)"
                    " VALUES(?,?,?,?,?)",
                    (prefix+"relation", universe_a, a, b, "Declared")
                )
                for table, key in (
                    ("fictional_calendars", calendar_a),
                    ("world_time_anchors", a),
                    ("world_time_precedences", prefix+"relation"),
                ):
                    _denied(
                        mem, f'UPDATE "{table}" SET id=id WHERE id=?',
                        (key,)
                    )
                    _denied(
                        mem, f'DELETE FROM "{table}" WHERE id=?',
                        (key,)
                    )
            case(immutability)
            if mem.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise FinalAuditStop("memory_integrity_changed")
            return tests


def perform(root: Path, custody: str, third: str, active: str,
            source_sha: str, logical_sha: str, backup_sha: str,
            custody_manifest_sha: str, third_sha: str, third_manifest_sha: str,
            sql_file: Path, sql_sha: str) -> dict:
    for value in (source_sha, logical_sha, backup_sha,
                  custody_manifest_sha, third_sha, third_manifest_sha, sql_sha):
        v7._hash(value)
    if root.name != "com.fabulaxiom.desktop":
        raise FinalAuditStop("unexpected_app_root")
    baseline = backup._check_baseline(root, active, source_sha, logical_sha)
    folder = v7._custody(root, custody)
    backup_path = folder / "fabulaxiom-pre-m3-1-v6.sqlite3"
    restored = folder / "isolated-restore-rehearsal-v6.sqlite3"
    old_manifest = folder / "manifest.json"
    new_dir = _third_folder(root, third)
    candidate = new_dir / "candidate-v7.sqlite3"
    new_manifest = new_dir / "candidate-v7-manifest.json"
    protected = (
        (backup_path, backup_sha),
        (restored, backup_sha),
        (old_manifest, custody_manifest_sha),
        (candidate, third_sha),
        (new_manifest, third_manifest_sha),
        (sql_file, sql_sha),
    )
    for path, digest in protected:
        audit._regular_file(path)
        if path.suffix == ".sqlite3":
            audit._reject_sidecars(path)
        if audit._file_sha256(path) != digest:
            raise FinalAuditStop("protected_sha256_mismatch")
    manifest = json.loads(new_manifest.read_text(encoding="utf-8"))
    if (manifest.get("protocol") != "m3_1_copy_only_v7_rehearsal_v1"
            or manifest.get("copy_file") != candidate.name
            or manifest.get("copy", {}).get("file_sha256") != third_sha
            or manifest.get("copy", {}).get("schema_version") != 7
            or manifest.get("source_production_sha256") != source_sha
            or manifest.get("source_v6_backup_sha256") != backup_sha
            or manifest.get("source_custody_manifest_sha256") != custody_manifest_sha
            or manifest.get("candidate_sql_sha256") != sql_sha
            or manifest.get("baseline_legacy_logical_sha256") != logical_sha
            or manifest.get("production_migrated") is not False
            or manifest.get("active_pointer_modified") is not False):
        raise FinalAuditStop("third_copy_manifest_links_invalid")
    expected_inventory = v7._expected_v7_inventory(
        backup_path, sql_file.read_text(encoding="utf-8")
    )
    verified = v7._validate_v7(candidate, baseline, expected_inventory)
    if verified["file_sha256"] != third_sha:
        raise FinalAuditStop("independent_candidate_sha_mismatch")
    scenarios = _exercise_time_constraints(candidate)
    if backup._check_baseline(root, active, source_sha, logical_sha) != baseline:
        raise FinalAuditStop("production_baseline_changed")
    for path, digest in protected:
        if audit._file_sha256(path) != digest:
            raise FinalAuditStop("file_changed_after_read_only_audit")
    return {
        "status": "PASS",
        "mode": "third_copy_read_only_plus_ram_constraints",
        "source_schema_version": 6,
        "third_copy_schema_version": 7,
        "candidate_sha256": third_sha,
        "candidate_sql_sha256": sql_sha,
        "legacy_tables_preserved": 14,
        "constraint_scenarios_passed": scenarios,
        "on_disk_sqlite_writes": False,
        "production_migrated": False,
        "active_pointer_modified": False,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--app-data-root", type=Path, required=True)
    p.add_argument("--custody-relative-dir", required=True)
    p.add_argument("--third-relative-dir", required=True)
    p.add_argument("--expected-active-file", required=True)
    p.add_argument("--expected-source-sha256", required=True)
    p.add_argument("--expected-logical-sha256", required=True)
    p.add_argument("--expected-backup-sha256", required=True)
    p.add_argument("--expected-custody-manifest-sha256", required=True)
    p.add_argument("--expected-third-sha256", required=True)
    p.add_argument("--expected-third-manifest-sha256", required=True)
    p.add_argument("--candidate-sql-file", type=Path, required=True)
    p.add_argument("--expected-candidate-sql-sha256", required=True)
    p.add_argument("--ack-app-stopped", action="store_true")
    opts = p.parse_args(argv)
    try:
        if not opts.ack_app_stopped:
            raise FinalAuditStop("operator_must_acknowledge_app_stopped")
        result = perform(
            opts.app_data_root, opts.custody_relative_dir, opts.third_relative_dir,
            opts.expected_active_file, opts.expected_source_sha256,
            opts.expected_logical_sha256, opts.expected_backup_sha256,
            opts.expected_custody_manifest_sha256, opts.expected_third_sha256,
            opts.expected_third_manifest_sha256, opts.candidate_sql_file,
            opts.expected_candidate_sql_sha256
        )
    except (FinalAuditStop, audit.AuditError, backup.BackupStop,
            v7.RehearsalStop, OSError, sqlite3.Error, ValueError,
            json.JSONDecodeError) as error:
        result = {
            "status": "FAIL", "reason": str(error) if isinstance(
                error, (FinalAuditStop, audit.AuditError,
                        backup.BackupStop, v7.RehearsalStop)
            ) else "independent_read_only_audit_error",
        }
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
