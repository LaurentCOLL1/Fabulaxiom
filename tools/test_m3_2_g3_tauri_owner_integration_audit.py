"""M3.2 G3: public-source-only Tauri owner-integration drift audit.

This deliberately reads repository Rust/Cargo text, never operator databases,
paths, sidecars, Windows ACLs or runtime configuration. Static checks are NOT
evidence of original-file provenance, journal quiescence or G3 eligibility.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUST = Path("src-tauri/src")


def source(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def rust_function(contents: str, signature: str) -> str:
    """A narrow top-level function extractor for known stable Rust source."""
    begin = contents.index(signature)
    end = contents.find("\n}\n", begin)
    if end == -1:
        raise AssertionError(f"Unterminated Rust function: {signature}")
    return contents[begin:end + 2]


class TauriOwnerIntegrationBoundaryTests(unittest.TestCase):
    def test_all_tauri_runners_have_no_managed_owner(self):
        lib = source(str(RUST / "lib.rs"))
        # Normal+M3.1 expose their previous handlers; the new fictional
        # third builder deliberately has ZERO invoke_handler registrations.
        self.assertEqual(lib.count("tauri::Builder::default()"), 3)
        self.assertEqual(lib.count(".invoke_handler("), 2)
        self.assertIn('#[cfg(all(feature = "m32-synthetic-preview", not(feature = "m31-isolated-preview")))]', lib)
        synthetic = lib.split("/** Distinct DEVELOPMENT-ONLY fictional UI shell.", 1)[1]
        synthetic = synthetic.split("\n#[cfg(test)]\nmod tests {", 1)[0]
        self.assertIn("tauri::Builder::default().run(context)", synthetic)
        self.assertNotIn(".invoke_handler(", synthetic)
        self.assertNotIn(".manage(", synthetic)
        self.assertNotIn("database::open_database(", synthetic)
        self.assertNotIn(".manage(", lib)
        self.assertNotIn(".setup(", lib)
        self.assertNotIn("tauri::State<", lib)
        self.assertNotIn("State<'_", lib)

    def test_no_owner_service_registered_as_normal_ipc(self):
        lib = source(str(RUST / "lib.rs"))
        normal = lib.split('#[cfg(not(any(feature = "m31-isolated-preview", feature = "m32-synthetic-preview")))]', 1)[1]
        normal = normal.split('/// Only one read-only command is registered.', 1)[0]
        self.assertIn("database_status,", normal)
        self.assertIn("create_database_backup,", normal)
        self.assertIn("restore_database_backup,", normal)
        self.assertNotIn("m32_owner", normal)
        self.assertNotIn("m32_g3", normal)
        self.assertNotIn("G3", normal)

    def test_database_status_opens_through_migrating_function(self):
        lib = source(str(RUST / "lib.rs"))
        body = rust_function(lib, "fn database_status(")
        self.assertIn("database::database_path", body)
        self.assertIn("database::open_database(&path)", body)

    def test_current_database_open_is_effectful_not_a_trusted_owner(self):
        db = source(str(RUST / "database.rs"))
        body = rust_function(db, "pub fn open_database(")
        self.assertIn("fs::create_dir_all(parent)?", body)
        self.assertIn("Connection::open(path)?", body)
        self.assertIn("run_migrations(&mut connection)?", body)
        self.assertIn("pub const CURRENT_SCHEMA_VERSION: i64 = 6;", db)
        self.assertIn("pub const MAX_AUTOMATIC_MIGRATION_VERSION: i64 = 6;", db)

    def test_hierarchy_and_entity_commands_open_per_call(self):
        for name in ("hierarchy_commands.rs", "entity_commands.rs"):
            with self.subTest(module=name):
                contents = source(str(RUST / name))
                body = rust_function(contents, "fn with_connection<T, F>(")
                self.assertIn("database::database_path(app)", body)
                self.assertIn("database::open_database(&path)", body)
                self.assertNotIn("State<", body)

    def test_app_backup_reopens_and_uses_path_based_vacuum(self):
        backups = source(str(RUST / "backup.rs"))
        create = rust_function(backups, "pub fn create_backup(")
        self.assertIn("database::open_database(&source_path)", create)
        self.assertIn("vacuum_copy(&connection, &destination)", create)
        vacuum = rust_function(backups, "fn vacuum_copy(")
        self.assertIn("VACUUM INTO", vacuum)
        reserve = rust_function(backups, "fn reserve_unique_file(")
        self.assertIn("create_new(true)", reserve)
        self.assertIn("drop(file)", reserve)
        # This released reservation is NOT a sealed new-only output handle.

    def test_existing_restore_is_not_an_approved_g3_path(self):
        backups = source(str(RUST / "backup.rs"))
        restore = rust_function(backups, "pub fn restore_backup(")
        self.assertIn("Connection::open_with_flags", restore)
        self.assertIn("activate_new_database", restore)
        self.assertIn("reserve_unique_file", restore)

    def test_toy_only_feature_and_compile_veto_remain(self):
        cargo = source("src-tauri/Cargo.toml")
        lib = source(str(RUST / "lib.rs"))
        self.assertIn("default = []", cargo)
        self.assertIn('m32-g3-owned-ram-toy = ["rusqlite/backup"]', cargo)
        self.assertIn(
            '#[cfg(all(feature = "m32-g3-owned-ram-toy", not(test)))]',
            lib,
        )
        self.assertIn(
            '#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]\nmod m32_owner_lifecycle_toy;',
            lib,
        )
        self.assertIn("compile_error!", lib)

    def test_existing_ram_owner_lifecycle_stays_test_only(self):
        toy = source(str(RUST / "m32_owner_lifecycle_toy.rs"))
        self.assertIn("Connection::open_in_memory()", toy)
        self.assertIn("Backup::new(source, &mut dest)", toy)
        self.assertIn("Mutex::new(OwnerSlot::new_invented", toy)
        self.assertIn("fn revoke(&mut self)", toy)
        self.assertNotIn("#[tauri::command]", toy)
        self.assertNotIn("Connection::open(", toy)
        self.assertNotIn("std::fs::", toy)


if __name__ == "__main__":
    unittest.main()
