"""M3.2 stage 18 — synthetic-only physical read-only SQLite v7 checks."""
import hashlib
from contextlib import closing, contextmanager
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

import m3_2_isolated_v7_physical_readonly as gate
from m3_2_operator_readonly_gate import GateStop


class V7ReadonlySyntheticTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="fabulaxiom-stage18-synthetic-only-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / "fabulaxiom.sqlite3"
        self.make_fixture()
        self.digest = gate._sha256(self.file)
        # Independent V6 baseline: copy only the disposable fixture into
        # memory, delete its seventh registry entry there, and use the ORIGINAL
        # source-controlled M3.1 V6 row-digest algorithm for all fourteen tables.
        # Computing the expected value with the new V7 checker itself would
        # reproduce the exact bug we are protecting against.
        with closing(sqlite3.connect(":memory:")) as baseline:
            with closing(sqlite3.connect(self.file)) as source:
                source.backup(baseline)
            baseline.execute("DELETE FROM schema_migrations WHERE version=7")
            baseline.commit()
            overall = hashlib.sha256(b"fabulaxiom-v6-typed-row-sha256-v1\0")
            for table in gate.v6.LEGACY_TABLES:
                _count, digest = gate.v6._logical_table(baseline, table)
                overall.update(table.encode("ascii") + b"\0" + bytes.fromhex(digest))
            self.logical = overall.hexdigest()

    @contextmanager
    def write_db(self):
        # Python sqlite3.Connection context manager does not close handles.
        # Explicit close is required, especially on Windows.
        with closing(sqlite3.connect(self.file)) as db:
            with db:
                yield db

    def make_fixture(self):
        with self.write_db() as db:
            db.execute("PRAGMA foreign_keys=OFF")
            db.execute("CREATE TABLE schema_migrations "
                       "(version INTEGER PRIMARY KEY, name TEXT NOT NULL) STRICT")
            db.execute("CREATE TABLE app_metadata "
                       "(key TEXT PRIMARY KEY, value TEXT NOT NULL) STRICT")
            db.execute("INSERT INTO app_metadata VALUES ('schema_owner','fabulaxiom')")
            db.executemany(
                "INSERT INTO schema_migrations VALUES(?,?)", gate.EXPECTED_LEDGER
            )
            for name in (*gate.v6.LEGACY_TABLES, *gate.v6.CANDIDATE_TABLES):
                if name in ("schema_migrations", "app_metadata"):
                    continue
                if name == "narrative_facts":
                    db.execute(
                        "CREATE TABLE narrative_facts "
                        "(id TEXT PRIMARY KEY, universe_id TEXT, "
                        "FOREIGN KEY(universe_id) REFERENCES universes(id)) STRICT"
                    )
                else:
                    db.execute('CREATE TABLE "' + name +
                               '" (id TEXT PRIMARY KEY NOT NULL) STRICT')
            db.execute("INSERT INTO universes VALUES('synthetic_universe')")
            db.execute(
                "INSERT INTO narrative_facts VALUES"
                "('synthetic_fact','synthetic_universe')"
            )
            db.commit()

    def snapshot(self):
        return {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in self.root.iterdir() if p.is_file()
        }

    def verify(self, digest=None, logical=None):
        return gate.inspect_file_readonly(
            self.file, digest or self.digest, logical or self.logical
        )

    def test_complete_v7_readonly_scan_and_no_file_writes(self):
        before = self.snapshot()
        result = self.verify()
        self.assertEqual(result["schema_version"], 7)
        self.assertEqual(result["physical_integrity"], "ok")
        self.assertEqual(result["foreign_key_violations"], 0)
        self.assertEqual(result["legacy_strict_tables"], 14)
        self.assertEqual(result["candidate_strict_empty_tables"], 3)
        self.assertTrue(result["typed_v6_logical_sha256_match"])
        self.assertFalse(result["sqlite_written"])
        self.assertEqual(self.snapshot(), before)

    def test_v7_seventh_ledger_row_does_not_change_legacy_v6_digest(self):
        with closing(sqlite3.connect(self.file)) as v7_conn:
            complete = v7_conn.execute(
                "SELECT version,name FROM schema_migrations ORDER BY version"
            ).fetchall()
            self.assertEqual(complete, gate.EXPECTED_LEDGER)
            self.assertEqual(gate._typed_v6_logical(v7_conn), self.logical)
            # The prior Stage 18 algorithm incorrectly hashed all seven
            # rows of schema_migrations as legacy data.
            all_rows = hashlib.sha256(b"fabulaxiom-v6-typed-row-sha256-v1\0")
            for table in gate.v6.LEGACY_TABLES:
                _, digest = gate.v6._logical_table(v7_conn, table)
                all_rows.update(table.encode("ascii") + b"\0" + bytes.fromhex(digest))
            self.assertNotEqual(all_rows.hexdigest(), self.logical)

    def test_changed_original_v6_row_still_vetoes_v7(self):
        with self.write_db() as db:
            db.execute(
                "UPDATE universes SET id='tampered_synthetic' "
                "WHERE id='synthetic_universe'"
            )
            db.execute(
                "UPDATE narrative_facts SET universe_id='tampered_synthetic' "
                "WHERE universe_id='synthetic_universe'"
            )
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "legacy_logical_digest_mismatch"):
            self.verify()

    def test_bad_pinned_file_sha_rejected_before_sqlite_open(self):
        with mock.patch.object(gate.sqlite3, "connect",
                               side_effect=AssertionError("must not connect")):
            with self.assertRaisesRegex(GateStop, "source_sha_mismatch"):
                self.verify(digest="f"*64)

    def test_bad_pinned_logical_v6_digest_rejected(self):
        with self.assertRaisesRegex(GateStop, "legacy_logical_digest_mismatch"):
            self.verify(logical="f"*64)

    def test_wrong_migration_ledger_refused(self):
        with self.write_db() as db:
            db.execute("UPDATE schema_migrations SET name='unexpected' WHERE version=7")
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "migration_ledger_not_exact"):
            self.verify()

    def test_missing_seventh_migration_refused(self):
        with self.write_db() as db:
            db.execute("DELETE FROM schema_migrations WHERE version=7")
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "migration_ledger_not_exact"):
            self.verify()

    def test_wrong_schema_owner_refused(self):
        with self.write_db() as db:
            db.execute(
                "UPDATE app_metadata SET value='wrong' WHERE key='schema_owner'"
            )
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "schema_owner_invalid"):
            self.verify()

    def test_foreign_key_violation_requires_separate_check(self):
        with self.write_db() as db:
            db.execute("PRAGMA foreign_keys=OFF")
            db.execute("INSERT INTO narrative_facts VALUES('orphan','nonexistent')")
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "foreign_key_check_failed"):
            self.verify()

    def test_missing_strict_v7_table_refused(self):
        with self.write_db() as db:
            db.execute("DROP TABLE fictional_calendars")
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "expected_strict_table_missing"):
            self.verify()

    def test_nonstrict_v7_table_refused(self):
        with self.write_db() as db:
            db.execute("DROP TABLE fictional_calendars")
            db.execute("CREATE TABLE fictional_calendars (id TEXT PRIMARY KEY)")
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "expected_strict_table_missing"):
            self.verify()

    def test_candidate_table_must_remain_empty(self):
        with self.write_db() as db:
            db.execute("INSERT INTO fictional_calendars VALUES('unexpected')")
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "candidate_table_not_empty"):
            self.verify()

    def test_sqlite_sidecar_present_refused_and_preserved(self):
        sidecar = Path(str(self.file) + "-wal")
        sidecar.write_bytes(b"synthetic sidecar; never delete")
        before = self.snapshot()
        with self.assertRaisesRegex(GateStop, "sqlite_sidecars_present"):
            self.verify()
        self.assertEqual(before, self.snapshot())

    def test_wal_header_refused_before_sqlite_open(self):
        payload = bytearray(self.file.read_bytes())
        payload[18:20] = b"\x02\x02"
        self.file.write_bytes(payload)
        self.digest = gate._sha256(self.file)
        with mock.patch.object(gate.sqlite3, "connect",
                               side_effect=AssertionError("must not open WAL")):
            with self.assertRaisesRegex(GateStop, "wal_or_unknown_header"):
                self.verify()

    def test_invalid_sqlite_header_refused(self):
        payload = bytearray(self.file.read_bytes())
        payload[:16] = b"not a sqlite db!"
        self.file.write_bytes(payload)
        self.digest = gate._sha256(self.file)
        with self.assertRaisesRegex(GateStop, "invalid_sqlite_header"):
            self.verify()

    def test_during_audit_digest_change_refused(self):
        original = gate._sha256
        checks = [0]
        def changing(path):
            checks[0] += 1
            return original(path) if checks[0] == 1 else "f"*64
        with mock.patch.object(gate, "_sha256", side_effect=changing):
            with self.assertRaisesRegex(GateStop, "changed_during_readonly_scan"):
                self.verify()

    def test_no_parent_custody_pass_means_no_sqlite_open(self):
        with mock.patch.object(gate.direct, "inspect",
                               side_effect=GateStop("source_custody_not_qualified")):
            with mock.patch.object(gate, "inspect_file_readonly",
                                   side_effect=AssertionError("must not open")):
                with self.assertRaisesRegex(GateStop, "source_custody_not_qualified"):
                    self.inspect_integration()

    def test_live_custody_gate_stays_pending_not_ready(self):
        m31 = self.root / gate.direct.M31_NAME
        target = m31 / "database" / "fabulaxiom.sqlite3"
        target.parent.mkdir(parents=True)
        target.write_bytes(self.file.read_bytes())
        with mock.patch.object(gate.direct, "inspect", return_value={
            "status": "PENDING_EXTERNAL_ATTESTATION",
            "roots_inspected": 4, "roles_checked": 26,
            "writes_performed": False, "m32_staging_authorized": False,
        }):
            with mock.patch.object(gate, "EXPECTED_CANDIDATE_SHA",
                                   gate._sha256(target)):
                with mock.patch.object(gate, "EXPECTED_LEGACY_LOGICAL", self.logical):
                    result = self.inspect_integration(m31=m31)
        self.assertEqual(result["status"], "PENDING_EXTERNAL_ATTESTATION")
        self.assertTrue(result["sqlite_opened_readonly"])
        self.assertTrue(result["sqlite_opened"])
        self.assertFalse(result["production_sqlite_opened"])
        self.assertFalse(result["m32_staging_authorized"])
        self.assertFalse(result["operator_live_qualified"])

    def inspect_integration(self, m31=None):
        parent = m31 or (self.root / gate.direct.M31_NAME)
        return gate.inspect(
            self.root, "a"*40, "b"*40, self.root/"com.fabulaxiom.desktop",
            self.root/"com.fabulaxiom.m25qual35fb842c", parent,
            self.root/"Fabulaxiom-M31-ACL-Evidence-4d520e18",
            "com.fabulaxiom.m32gate"+"e"*32, True,
            token_checker=lambda: True
        )


if __name__ == "__main__":
    unittest.main()
