"""G3 transactional Online Backup from pre-opened FICTIONAL owner, never originals."""
from contextlib import closing
from dataclasses import replace
import hashlib
import sqlite3
from pathlib import Path
import unittest
from unittest import mock

from m3_2_g3_win_full_toy_cycle import (
    SNAPSHOT_DIR, RESTORE_DIR, SNAPSHOT_NAME, ToyCeremonyVeto,
    _new_dir, _write_new_snapshot, restore_toy,
)
from m3_2_g3_owned_online_backup_toy import (
    _TOY_ISSUER, OwnedToyVeto, invented_toy_owner, backup_owner_to_ram,
    sealed_owned_toy_cycle, OwnedToy, self_test
)


class OwnedConnectionBackupTests(unittest.TestCase):
    def test_full_cycle_v6(self):
        with invented_toy_owner(6) as owner:
            result = sealed_owned_toy_cycle(owner)
            self.assertEqual(result["scope"], "INVENTED_OWNER_TOY_ONLY")
            self.assertEqual(result["sha256"], result["snapshot_sha256"])
            self.assertTrue(result["third_location_restored"])
            self.assertFalse(result["real_g3_authorized"])

    def test_full_cycle_v7(self):
        with invented_toy_owner(7) as owner:
            result = sealed_owned_toy_cycle(owner)
            self.assertEqual(result["strategy"], "ONLINE_BACKUP_EXISTING_OWNER_TO_RAM")
            self.assertEqual(result["real_source_provenance"], "UNPROVEN")

    def test_no_source_sqlite_reopen_in_backup(self):
        with invented_toy_owner(6) as owner:
            actual = sqlite3.connect
            opened = []
            def observe(path, *args, **kwargs):
                opened.append(str(path))
                return actual(path, *args, **kwargs)
            with mock.patch("sqlite3.connect", side_effect=observe):
                image, info = backup_owner_to_ram(owner)
            self.assertTrue(opened)
            self.assertEqual(set(opened), {":memory:"})
            self.assertEqual(info["source_connection_reopened"], False)
            self.assertTrue(image.startswith(b"SQLite format 3\x00"))

    def test_existing_connection_still_usable_after_capture(self):
        with invented_toy_owner(6) as owner:
            source_change_before = owner.connection.total_changes
            backup_owner_to_ram(owner)
            self.assertEqual(owner.connection.execute("SELECT COUNT(*) FROM imagined_books").fetchone()[0], 1)
            self.assertEqual(owner.connection.total_changes, source_change_before)

    def test_uncommitted_source_owner_transaction_rejected(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("UPDATE imagined_books SET title='Uncommitted' WHERE id=1")
            with self.assertRaisesRegex(OwnedToyVeto, "uncommitted"):
                backup_owner_to_ram(owner)
            owner.connection.rollback()
            self.assertFalse((owner.root / SNAPSHOT_DIR).exists())

    def test_source_connection_closed_rejected(self):
        with invented_toy_owner(6) as owner:
            owner.connection.close()
            with self.assertRaisesRegex(OwnedToyVeto, "unavailable"):
                backup_owner_to_ram(owner)

    def test_forged_owner_token_rejected(self):
        with invented_toy_owner(6) as owner:
            fake = replace(owner, issuer=object())
            with self.assertRaisesRegex(OwnedToyVeto, "fixture-issued"):
                backup_owner_to_ram(fake)

    def test_replaced_connection_does_not_match_toy_source(self):
        with invented_toy_owner(6) as owner:
            with closing(sqlite3.connect(":memory:")) as rogue:
                fake = replace(owner, connection=rogue)
                with self.assertRaisesRegex(OwnedToyVeto, "different source"):
                    backup_owner_to_ram(fake)

    def test_unqualified_attached_database_rejected(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("ATTACH DATABASE ':memory:' AS toy_attached")
            with self.assertRaisesRegex(OwnedToyVeto, "attached"):
                backup_owner_to_ram(owner)
            owner.connection.execute("DETACH DATABASE toy_attached")

    def test_wrong_migration_rejected_before_disk_write(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("DELETE FROM schema_migrations WHERE version=6")
            owner.connection.commit()
            with self.assertRaisesRegex(OwnedToyVeto, "schema_migrations"):
                sealed_owned_toy_cycle(owner)
            self.assertFalse((owner.root / SNAPSHOT_DIR).exists())

    def test_orphan_foreign_key_rejected_before_disk_write(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("PRAGMA foreign_keys=OFF")
            owner.connection.execute("UPDATE invented_facts SET book_id=999 WHERE id=1")
            owner.connection.commit()
            with self.assertRaisesRegex(OwnedToyVeto, "foreign-key"):
                sealed_owned_toy_cycle(owner)
            self.assertFalse((owner.root / SNAPSHOT_DIR).exists())

    def test_inadequate_memory_budget_rejected(self):
        with invented_toy_owner(6) as owner:
            with self.assertRaisesRegex(OwnedToyVeto, "memory budget"):
                backup_owner_to_ram(owner, max_bytes=1024)
            self.assertFalse((owner.root / SNAPSHOT_DIR).exists())

    def test_existing_snapshot_file_collision_preserved(self):
        with invented_toy_owner(6) as owner:
            image, _ = backup_owner_to_ram(owner)
            out = _new_dir(owner.root, SNAPSHOT_DIR)
            destination = out / SNAPSHOT_NAME
            destination.write_bytes(b"DO-NOT-REPLACE")
            with self.assertRaises(ToyCeremonyVeto):
                _write_new_snapshot(out, image)
            self.assertEqual(destination.read_bytes(), b"DO-NOT-REPLACE")

    def test_existing_destination_directory_collision_preserved(self):
        with invented_toy_owner(6) as owner:
            _new_dir(owner.root, SNAPSHOT_DIR)
            sentinel = owner.root / SNAPSHOT_DIR / "sentinel"
            sentinel.write_text("EXISTING")
            with self.assertRaisesRegex(ToyCeremonyVeto, "collision"):
                sealed_owned_toy_cycle(owner)
            self.assertEqual(sentinel.read_text(), "EXISTING")

    def test_restore_existing_directory_refuses_preserves_sentinel(self):
        with invented_toy_owner(6) as owner:
            image, _ = backup_owner_to_ram(owner)
            out = _new_dir(owner.root, SNAPSHOT_DIR)
            _write_new_snapshot(out, image)
            restored = _new_dir(owner.root, RESTORE_DIR)
            sentinel = restored / SNAPSHOT_NAME
            sentinel.write_bytes(b"KEEP")
            with self.assertRaisesRegex(ToyCeremonyVeto, "collision"):
                restore_toy(owner.root, image, 6)
            self.assertEqual(sentinel.read_bytes(), b"KEEP")

    def test_corrupt_snapshot_prevents_restore(self):
        with invented_toy_owner(6) as owner:
            image, _ = backup_owner_to_ram(owner)
            out = _new_dir(owner.root, SNAPSHOT_DIR)
            _write_new_snapshot(out, image)
            snapshot = out / SNAPSHOT_NAME
            snapshot.write_bytes(b"CORRUPTED-ONLY-TOY")
            with self.assertRaisesRegex(ToyCeremonyVeto, "mutated"):
                restore_toy(owner.root, image, 6)
            self.assertFalse((owner.root / RESTORE_DIR).exists())

    def test_wal_owner_uses_transactional_copy_and_normalizes_ram(self):
        with invented_toy_owner(6) as owner:
            journal_mode = owner.connection.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            self.assertEqual(journal_mode.lower(), "wal")
            image, report = backup_owner_to_ram(owner)
            self.assertTrue(report["ram_vacuum_normalized_wal_header"])
            self.assertEqual(image[18:20], b"\x01\x01")
            self.assertEqual(owner.connection.execute("PRAGMA journal_mode").fetchone()[0], "wal")

    def test_wal_committed_writer_observed_in_new_snapshot(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("PRAGMA journal_mode=WAL")
            with closing(sqlite3.connect(owner.source)) as writer, writer:
                writer.execute("UPDATE invented_facts SET detail='Updated committed' WHERE id=1")
            image, _ = backup_owner_to_ram(owner)
            with closing(sqlite3.connect(":memory:")) as restored:
                restored.deserialize(image)
                value = restored.execute("SELECT detail FROM invented_facts WHERE id=1").fetchone()[0]
            self.assertEqual(value, "Updated committed")

    def test_wal_uncommitted_other_writer_not_in_snapshot(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("PRAGMA journal_mode=WAL")
            with closing(sqlite3.connect(owner.source)) as writer:
                writer.execute("UPDATE invented_facts SET detail='NOT COMMITTED' WHERE id=1")
                try:
                    image, _ = backup_owner_to_ram(owner)
                finally:
                    writer.rollback()
            with closing(sqlite3.connect(":memory:")) as restored:
                restored.deserialize(image)
                value = restored.execute("SELECT detail FROM invented_facts WHERE id=1").fetchone()[0]
            self.assertEqual(value, "Example")

    def test_snapshot_remains_stable_after_later_writer_commit(self):
        with invented_toy_owner(6) as owner:
            owner.connection.execute("PRAGMA journal_mode=WAL")
            image, _ = backup_owner_to_ram(owner)
            with closing(sqlite3.connect(owner.source)) as writer, writer:
                writer.execute("UPDATE invented_facts SET detail='Later' WHERE id=1")
            with closing(sqlite3.connect(":memory:")) as recovered:
                recovered.deserialize(image)
                self.assertEqual(recovered.execute("SELECT detail FROM invented_facts").fetchone()[0], "Example")
            self.assertEqual(owner.connection.execute("SELECT detail FROM invented_facts").fetchone()[0], "Later")

    def test_ram_serialized_output_hash_matches_restored_copy(self):
        with invented_toy_owner(7) as owner:
            report = sealed_owned_toy_cycle(owner)
            snapshot = owner.root / SNAPSHOT_DIR / SNAPSHOT_NAME
            restored = owner.root / RESTORE_DIR / SNAPSHOT_NAME
            self.assertEqual(snapshot.read_bytes(), restored.read_bytes())
            self.assertEqual(hashlib.sha256(snapshot.read_bytes()).hexdigest(), report["sha256"])

    def test_no_current_rust_migration_path_invocation(self):
        from m3_2_g3_source_strategy_policy import classify, Evidence, Strategy
        verdict = classify(Strategy.APP_OWNED_BACKUP, Evidence())
        self.assertFalse(verdict.real_g3_authorized)
        self.assertFalse(verdict.design_review_candidate)

    def test_self_test_never_authorizes_real_g3(self):
        self_test()


if __name__ == "__main__":
    unittest.main()
