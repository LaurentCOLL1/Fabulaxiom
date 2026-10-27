"""Adversarial source-only tests of broad textual SQLite-site inventory.

Runs in CI on checked-in Rust text and invented mutations; never opens SQLite.
"""
import unittest
from pathlib import Path
from m32_rust_sqlite_open_inventory import (
    ROOT, TREE, EXPECTED, ReviewRequired, audit_inventory, repository_inventory,
)

def source_map():
    return {
        p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(TREE.rglob("*.rs"))
    }

class RustSqliteOpenInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = source_map()

    def veto(self, path, code):
        changed = dict(self.src)
        changed[path] = changed.get(path, "") + "\n" + code + "\n"
        with self.assertRaises(ReviewRequired):
            audit_inventory(changed)

    def test_01_repository_scan_match_never_proves_writer_absence(self):
        a=repository_inventory()
        self.assertEqual(a["writer_absence"],"NOT_PROVEN")
        self.assertEqual(a["real_g3"],"STOP_UNAVAILABLE")
        self.assertFalse(a["real_g3_authorized"])
        self.assertFalse(a["originals_opened"])
        self.assertEqual(a["matched_files"],len(EXPECTED))

    def test_02_verified_known_sources_match(self):
        self.assertEqual(audit_inventory(self.src)["operator_execution"],"NOT_AUTHORIZED")

    def test_03_new_rust_file_with_sqlite_open_veto(self):
        self.veto("src-tauri/src/brand_new.rs","Connection::open(path)?;")

    def test_04_existing_untracked_rust_file_veto(self):
        self.veto("src-tauri/src/main.rs","Connection::open_with_flags(path, flags)?;")

    def test_05_new_application_open_database_call_veto(self):
        self.veto("src-tauri/src/facts.rs","database::open_database(&path)?;")

    def test_06_new_migration_call_veto(self):
        self.veto("src-tauri/src/entity.rs","run_migrations(&mut conn)?;")

    def test_07_new_vacuum_into_veto(self):
        self.veto("src-tauri/src/revisions.rs",'let query = "VACUUM INTO ?1";')

    def test_08_new_attach_database_veto(self):
        self.veto("src-tauri/src/backup.rs", 'let stmt = "ATTACH DATABASE ?1 AS temp";')

    def test_09_new_open_create_flag_veto(self):
        self.veto("src-tauri/src/main.rs","OpenFlags::SQLITE_OPEN_CREATE")

    def test_10_new_raw_ffi_sqlite_open_veto(self):
        self.veto("src-tauri/src/main.rs","unsafe { sqlite3_open_v2(ptr) }")

    def test_11_new_backup_api_marker_veto(self):
        self.veto("src-tauri/src/main.rs","backup::Backup::new(&source, &dest)")

    def test_12_removing_known_call_requires_reaudit(self):
        changed = dict(self.src)
        name = "src-tauri/src/database.rs"
        self.assertIn("Connection::open(path)?;", changed[name])
        changed[name] = changed[name].replace("Connection::open(path)?;", "safe_nonmigrating_open(path)?;", 1)
        with self.assertRaises(ReviewRequired):
            audit_inventory(changed)

    def test_13_new_unrelated_file_allowed_but_no_gate_pass(self):
        changed = dict(self.src)
        changed["src-tauri/src/new_unrelated.rs"] = "pub fn hello() -> bool { true }"
        self.assertFalse(audit_inventory(changed)["real_g3_authorized"])

    def test_14_reject_path_escape(self):
        self.veto("src-tauri/src/../private.rs","Connection::open(path)?;")

    def test_15_reject_bad_input_type(self):
        with self.assertRaises(ReviewRequired):
            audit_inventory({"src-tauri/src/test.rs": 9})

    def test_16_empty_inventory_denied(self):
        with self.assertRaises(ReviewRequired):
            audit_inventory({})

    def test_17_new_file_without_extension_rejected_even_if_sqlite(self):
        self.veto("src-tauri/src/new.txt","Connection::open(path)?;")

    def test_19_new_disk_open_in_reviewed_ram_module_is_vetoed(self):
        self.veto("src-tauri/src/m32_manual_chronology.rs",
                  "Connection::open(user_path)?;")

    def test_20_new_migration_in_reviewed_ram_module_is_vetoed(self):
        self.veto("src-tauri/src/m32_manual_chronology.rs",
                  "run_migrations(&mut another_connection)?;")

    def test_21_reviewed_module_is_ram_only_without_tauri_ipc(self):
        content = self.src["src-tauri/src/m32_manual_chronology.rs"]
        self.assertEqual(content.count("Connection::open_in_memory()"), 1)
        self.assertEqual(content.count("database::run_migrations("), 1)
        for forbidden in ("Connection::open(", "Connection::open_with_flags(",
                          "database::open_database(", "#[tauri::command]",
                          "std::fs::File::open(", "SQLITE_OPEN_CREATE"):
            self.assertNotIn(forbidden, content)
        lib = self.src["src-tauri/src/lib.rs"]
        self.assertIn("#[cfg(test)]" + chr(10) + "mod m32_manual_chronology;", lib)
        self.assertEqual(audit_inventory(self.src)["writer_absence"], "NOT_PROVEN")

    def test_18_all_fictional_positive_larger_inventory_never_authorizes_g3(self):
        self.assertEqual(audit_inventory(self.src)["review"],"EXACT_KNOWN_TEXT_COUNTS_MATCH_NOT_EXHAUSTIVE")
        self.assertEqual(audit_inventory(self.src)["real_g3"],"STOP_UNAVAILABLE")


    def test_22_only_reviewed_invented_uri_ram_opens_added(self):
        p = "src-tauri/src/m32_preopened_query_only_toy.rs"
        source = self.src[p]
        self.assertEqual(EXPECTED[p], (3, 0, 0, 0, 2, 3, 0))
        self.assertIn("mode=memory&cache=shared", source)
        self.assertIn("NEXT_INVENTED_RAM.fetch_add", source)
        self.assertEqual(source.count("Connection::open_with_flags(&uri, flags)?"), 2)
        self.assertIn("SQLITE_OPEN_URI", source)
        self.assertNotIn("std::fs::", source)
        self.assertNotIn("#[tauri::command]", source)
        self.assertNotIn("Connection::open(user_path)", source)
        self.assertEqual(audit_inventory(self.src)["writer_absence"], "NOT_PROVEN")
        self.assertFalse(audit_inventory(self.src)["real_g3_authorized"])

    def test_23_future_unreviewed_disk_open_in_toy_still_vetoed(self):
        self.veto("src-tauri/src/m32_preopened_query_only_toy.rs",
                  "Connection::open(operator_path)?;")


    def test_24_greenfield_new_data_only_calls_are_reviewed_and_test_scoped(self):
        p = "src-tauri/src/greenfield_smoke_tests.rs"
        source = self.src[p]
        self.assertEqual(EXPECTED[p], (0, 16, 0, 0, 0, 0, 0))
        self.assertEqual(source.count("database::open_database("), 16)
        self.assertIn("std::env::temp_dir()", source)
        self.assertIn("fs::create_dir(&root)", source)
        self.assertIn("fabulaxiom-ci-greenfield-", source)
        self.assertIn("let restored_root = new_ci_only_root(", source)
        self.assertIn("backup::restore_backup(&restored_root,", source)
        for forbidden in ("#[tauri::command]", "Connection::open(",
                          "Connection::open_with_flags(", "SQLITE_OPEN_CREATE",
                          "app_local_data_dir()", "std::env::var("):
            self.assertNotIn(forbidden, source)
        lib = self.src["src-tauri/src/lib.rs"]
        self.assertIn("#[cfg(test)]" + chr(10) + "mod greenfield_smoke_tests;", lib)
        self.assertEqual(audit_inventory(self.src)["writer_absence"], "NOT_PROVEN")

    def test_25_unreviewed_thirteenth_greenfield_open_requires_reaudit(self):
        self.veto("src-tauri/src/greenfield_smoke_tests.rs",
                  "database::open_database(operator_path)?;")

if __name__ == "__main__":
    unittest.main()
