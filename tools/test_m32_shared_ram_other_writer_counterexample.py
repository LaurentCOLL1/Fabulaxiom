"""M3.2: adversarial SQLITE RAM concurrency proof-of-insufficiency only.

Runs only on a hard-coded SQLite URI with *mode=memory*, uri=True and
cache=shared. No operator path, filesystem database, Windows processes,
Tauri runtime, migration or external network. Nothing here grants G2B/G3.
"""
import sqlite3
import unittest

# The exact fixed URI uses SQLite's documented named RAM-only mode.
# Do not replace mode=memory with a disk URI or user-controlled path.
RAM_URI = "file:fabulaxiom_m32_only_fictional_ram_concurrency?mode=memory&cache=shared"

def refusal_result(reader: sqlite3.Connection) -> dict[str, object]:
    """Never elevate any metadata or toy observation to a real writer proof."""
    return {
        "reader_query_only": reader.execute("PRAGMA query_only").fetchone()[0] == 1,
        "reader_total_changes": reader.total_changes,
        "real_writer_absence": "NOT_PROVEN",
        "real_g3": "STOP_UNAVAILABLE",
        "g2b_to_g6": "NOT_AUTHORIZED",
        "real_g3_authorized": False,
    }

class SharedRAMWriterCounterexamples(unittest.TestCase):
    def setUp(self):
        self.reader = sqlite3.connect(RAM_URI, uri=True, isolation_level=None)
        self.writer = sqlite3.connect(RAM_URI, uri=True, isolation_level=None)
        self.addCleanup(self.writer.close)
        self.addCleanup(self.reader.close)
        for conn in (self.reader, self.writer):
            dbs = conn.execute("PRAGMA database_list").fetchall()
            self.assertEqual([(name, path) for _id, name, path in dbs],
                             [("main", "")], "STOP: disk or unexpected ATTACH")
        self.writer.execute(
            "CREATE TABLE invented_events("
            "id INTEGER PRIMARY KEY, detail TEXT NOT NULL)"
        )
        self.writer.execute("INSERT INTO invented_events VALUES (1, 'before')")
        self.reader.execute("PRAGMA query_only=ON")

    def test_01_two_separate_connections_share_only_ram(self):
        self.assertEqual(self.reader.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 1)
        self.assertEqual(self.writer.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 1)
        self.assertIsNot(self.reader, self.writer)

    def test_02_query_only_rejects_reader_insert(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.reader.execute("INSERT INTO invented_events VALUES (2, 'forbidden')")
        self.assertEqual(self.writer.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 1)

    def test_03_query_only_rejects_reader_update_and_delete(self):
        for sql in ("UPDATE invented_events SET detail='wrong'",
                    "DELETE FROM invented_events"):
            with self.assertRaises(sqlite3.OperationalError):
                self.reader.execute(sql)
        self.assertEqual(self.writer.execute("SELECT detail FROM invented_events").fetchone()[0], "before")

    def test_04_external_writer_inserts_while_reader_query_only(self):
        self.assertEqual(self.reader.execute("PRAGMA query_only").fetchone()[0], 1)
        self.writer.execute("INSERT INTO invented_events VALUES (2, 'external')")
        self.assertEqual(self.reader.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 2)
        self.assertEqual(self.reader.execute("PRAGMA query_only").fetchone()[0], 1)

    def test_05_external_insert_does_not_change_reader_total_changes(self):
        before = self.reader.total_changes
        self.writer.execute("INSERT INTO invented_events VALUES (2, 'outside')")
        self.assertEqual(self.reader.total_changes, before)
        self.assertEqual(self.reader.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 2)

    def test_06_external_update_does_not_change_reader_total_changes(self):
        before = self.reader.total_changes
        self.writer.execute("UPDATE invented_events SET detail='changed' WHERE id=1")
        self.assertEqual(self.reader.total_changes, before)
        self.assertEqual(self.reader.execute("SELECT detail FROM invented_events").fetchone()[0], "changed")

    def test_07_external_delete_does_not_change_reader_total_changes(self):
        before = self.reader.total_changes
        self.writer.execute("DELETE FROM invented_events WHERE id=1")
        self.assertEqual(self.reader.total_changes, before)
        self.assertEqual(self.reader.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 0)

    def test_08_data_version_can_notice_other_connection_commit(self):
        before = self.reader.execute("PRAGMA data_version").fetchone()[0]
        self.writer.execute("INSERT INTO invented_events VALUES (2, 'outside')")
        after = self.reader.execute("PRAGMA data_version").fetchone()[0]
        self.assertNotEqual(before, after)
        self.assertEqual(refusal_result(self.reader)["real_writer_absence"], "NOT_PROVEN")

    def test_09_reader_query_only_does_not_turn_writer_query_only(self):
        self.assertEqual(self.reader.execute("PRAGMA query_only").fetchone()[0], 1)
        self.assertEqual(self.writer.execute("PRAGMA query_only").fetchone()[0], 0)
        self.writer.execute("INSERT INTO invented_events VALUES (2, 'still writable')")
        self.assertEqual(self.reader.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 2)

    def test_10_external_schema_change_cannot_promote_writer_absence(self):
        before = self.reader.total_changes
        self.writer.execute("CREATE TABLE wholly_invented_extra(id INTEGER PRIMARY KEY)")
        self.assertEqual(self.reader.total_changes, before)
        count = self.reader.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name='wholly_invented_extra'"
        ).fetchone()[0]
        self.assertEqual(count, 1)
        self.assertEqual(refusal_result(self.reader)["real_g3"], "STOP_UNAVAILABLE")

    def test_11_even_no_external_mutation_does_not_prove_future_quiescence(self):
        state = refusal_result(self.reader)
        self.assertTrue(state["reader_query_only"])
        self.assertFalse(state["real_g3_authorized"])
        self.assertEqual(state["g2b_to_g6"], "NOT_AUTHORIZED")

    def test_12_all_positive_local_observations_still_refuse_real_g3(self):
        self.writer.execute("INSERT INTO invented_events VALUES (2, 'other writer')")
        state = refusal_result(self.reader)
        self.assertEqual(state["real_writer_absence"], "NOT_PROVEN")
        self.assertEqual(state["real_g3"], "STOP_UNAVAILABLE")
        self.assertFalse(state["real_g3_authorized"])
        self.assertEqual(self.reader.execute("SELECT COUNT(*) FROM invented_events").fetchone()[0], 2)

if __name__ == "__main__":
    unittest.main()
