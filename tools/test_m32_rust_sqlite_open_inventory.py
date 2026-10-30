"""Adversarial source-only tests of broad textual SQLite-site inventory.

Runs in CI on checked-in Rust text and invented mutations; never opens SQLite.
"""
import unittest
from pathlib import Path
from m32_rust_sqlite_open_inventory import (
    ROOT, TREE, EXPECTED, ReviewRequired, audit_inventory, repository_inventory, counts,
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
        self.assertEqual(EXPECTED[p], (0, 27, 0, 0, 0, 0, 0))
        self.assertEqual(source.count("database::open_database("), 27)
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

    def test_25_unreviewed_next_greenfield_open_requires_reaudit(self):
        self.veto("src-tauri/src/greenfield_smoke_tests.rs",
                  "database::open_database(operator_path)?;")

    def test_26_new_only_os_exclusive_claim_remains_test_scoped(self):
        p = "src-tauri/src/world_time_file_migration_tests.rs"
        source = self.src[p]
        self.assertEqual(EXPECTED[p], (20, 4, 3, 2, 0, 8, 0))
        self.assertIn("fn open_new_only_disposable_file(path: &Path)", source)
        self.assertIn("options.write(true).create_new(true)", source)
        self.assertIn("options.open(path)", source)
        self.assertIn("OpenFlags::SQLITE_OPEN_READ_WRITE", source)
        self.assertNotIn("OpenFlags::SQLITE_OPEN_CREATE", source)
        self.assertNotIn("#[tauri::command]", source)
        self.assertIn("std::env::temp_dir()", source)
        self.assertIn("mod world_time_file_migration_tests;", self.src["src-tauri/src/lib.rs"])

    def test_27_new_only_refusal_matrix_keeps_sidecars_and_prior_v6(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        for signal in ("symlink_metadata", "ErrorKind::NotFound", "-wal", "-shm", "-journal",
                       "m32_new_only_claim_refuses_existing_file_directory_and_orphan_sidecars",
                       "m32_exclusive_new_file_claim_builds_test_only_v7_and_reopen_cannot_reclaim_it",
                       "m32_exclusive_claim_two_concurrent_creators_only_one_wins",
                       "assert_eq!(fs::read(&previous).unwrap(), previous_bytes",
                       "assert!(!root.file(\"activation\").exists())"):
            self.assertIn(signal, source)

    def test_28_other_unreviewed_creation_flag_remains_vetoed(self):
        self.veto("src-tauri/src/world_time_file_migration_tests.rs",
                  "Connection::open_with_flags(operator_path, OpenFlags::SQLITE_OPEN_CREATE)?;")

    def test_29_windows_handoff_keeps_claim_and_parent_pinned_until_sqlite_open(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        self.assertIn("fn pin_disposable_parent(path: &Path)", source)
        self.assertIn(".custom_flags(0x0200_0000)", source)
        self.assertIn("options.share_mode(0x0000_0001 | 0x0000_0002)", source)
        self.assertIn("fn connect_claimed_disposable_file(path: &Path, claim: fs::File)", source)
        opened = source.index("let connection = Connection::open_with_flags(path")
        released = source.index("drop(claim);", opened)
        self.assertLess(opened, released)
        self.assertIn("m32_windows_pinned_fixture_parent_and_claim_refuse_rename_during_open", source)

    def test_30_parent_namespace_counterexample_does_not_claim_production_proof(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        self.assertIn("m32_unpinned_parent_name_can_be_replaced_before_new_only_claim", source)
        self.assertIn("NEGATIVE witness: future production admission MUST veto root replacement", source)
        self.assertNotIn("#[tauri::command]", source)
        self.assertEqual(audit_inventory(self.src)["real_g3"], "STOP_UNAVAILABLE")

    def test_31_disposable_root_lexical_child_guard_refuses_escape_and_devices(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        for signal in ("fn checked_fixture_parent_chain(root: &Path, destination: &Path)",
                       "destination.strip_prefix(root)", "Component::Normal",
                       "non-normal destination component", "forbidden_device_name",
                       "CON", "COM", "LPT", "stream:ads.sqlite3",
                       "m32_owned_fixture_path_guard_refuses_escape_and_unsafe_components"):
            self.assertIn(signal, source)
        self.assertNotIn("app_local_data_dir()", source)
        self.assertEqual(EXPECTED["src-tauri/src/world_time_file_migration_tests.rs"],
                         (20, 4, 3, 2, 0, 8, 0))

    def test_32_windows_fixture_chain_uses_held_file_identity_and_reparse_veto(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        for signal in ("fn pin_checked_fixture_chain(root: &Path, destination: &Path)",
                       "fn revalidate_checked_fixture_chain(root: &Path, destination: &Path, pins: &[fs::File])",
                       "FILE_FLAG_OPEN_REPARSE_POINT", "FILE_ATTRIBUTE_REPARSE_POINT",
                       "const FILE_READ_ATTRIBUTES: u32 = 0x0000_0080",
                       ".access_mode(FILE_READ_ATTRIBUTES)",
                       "unsafe extern \"system\"", "GetFileInformationByHandle",
                       "windows_fixture_handle_identity(&before_handle)",
                       "windows_fixture_handle_identity(&pin)",
                       "windows_fixture_handle_identity(&after_handle)", "pin.metadata()",
                       "before_id != held_id", "after_id != held_id",
                       "m32_windows_owned_fixture_chain_rechecks_substitution_before_sqlite",
                       "revalidate_checked_fixture_chain(&root.0, &destination, &pins).is_err()",
                       "fs::create_dir(&second).expect(\"disposable replacement leaf only\")"):
            self.assertIn(signal, source)
        self.assertNotIn("m.volume_serial_number()?", source)
        self.assertNotIn("m.file_index()?", source)
        self.assertNotIn("#[tauri::command]", source)
        self.assertEqual(audit_inventory(self.src)["writer_absence"], "NOT_PROVEN")

    def test_33_windows_native_vfs_handle_comparison_is_post_xopen_and_test_only(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        for signal in ("fn sqlite_windows_fixture_opened_identity(db: &Connection)",
                       "rusqlite::ffi::sqlite3_file_control(",
                       "rusqlite::ffi::SQLITE_FCNTL_WIN32_GET_HANDLE",
                       "fn windows_fixture_raw_handle_identity(handle:",
                       "fn open_windows_fixture_with_post_xopen_identity_check(",
                       "SQLite VFS opened a different fixture file identity",
                       "m32_windows_sqlite_vfs_handle_matches_live_exclusive_fixture_claim"):
            self.assertIn(signal, source)
        self.assertNotIn("#[tauri::command]", source)
        self.assertEqual(audit_inventory(self.src)["real_g3"], "STOP_UNAVAILABLE")

    def test_34_postcheck_name_swap_proves_no_atomic_sqlite_handoff(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        for signal in ("m32_windows_sqlite_vfs_native_handle_detects_post_check_name_substitution",
                       "drop(claim);", "fs::rename(&destination, &displaced)",
                       "revalidate_checked_fixture_chain(&root.0, &destination, &pins).is_ok()",
                       "open_windows_fixture_with_post_xopen_identity_check(&destination, original_id).is_err()",
                       "SQLite xOpen HAS ALREADY happened"):
            self.assertIn(signal, source)
        self.assertEqual(EXPECTED["src-tauri/src/world_time_file_migration_tests.rs"],
                         (20, 4, 3, 2, 0, 8, 0))

    def test_35_win32_fileidinfo_128_is_test_only_not_a_hello_or_atomic_gate(self):
        source = self.src["src-tauri/src/world_time_file_migration_tests.rs"]
        for marker in ("fn windows_fixture_raw_file_id_128(handle:",
                       "GetFileInformationByHandleEx(", "FILE_ID_INFO_CLASS: i32 = 0x12",
                       "struct WinFileIdInfo", "file_id: [u8; 16]",
                       "fn sqlite_windows_fixture_opened_file_id_128(db: &Connection)",
                       "m32_windows_sqlite_fileid_128_matches_claim_but_cannot_prevent_prior_swap",
                       "assert_ne!(original_id, replacement_id)",
                       "assert_eq!(sqlite_windows_fixture_opened_file_id_128(&followed).unwrap(), replacement_id)"):
            self.assertIn(marker, source)
        self.assertNotIn("UserConsentVerifier", source,
                         "no Windows Hello runtime authorization is part of this fixture")
        self.assertNotIn("#[tauri::command]", source)
        self.assertEqual(audit_inventory(self.src)["real_g3"], "STOP_UNAVAILABLE")

    def test_36_single_user_hello_boundary_is_cfg_test_policy_only(self):
        module = "src-tauri/src/m32_sensitive_action_consent_tests.rs"
        source = self.src[module]
        main = self.src["src-tauri/src/lib.rs"]
        self.assertIn("#[cfg(test)]\nmod m32_sensitive_action_consent_tests;", main)
        for signal in ("struct ExactIntent", "enum SensitiveAction", "enum TrustedOsOutcome",
                       "fn request(", "fn apply_fixture(", "self.pending.take()",
                       "ConsentExpired", "IntentChanged", "RevalidationFailed",
                       "m32_hello_fixture_every_nonverified_os_outcome_stops_and_consumes",
                       "m32_hello_fixture_revision_change_fails_closed"):
            self.assertIn(signal, source)
        for forbidden in ("#[tauri::command]", "RequestVerificationForWindowAsync(hwnd,",
                          "UserConsentVerifier::Request", "Connection::open(",
                          "database::open_database(", "SQLITE_OPEN_CREATE"):
            self.assertNotIn(forbidden, source)
        self.assertEqual(audit_inventory(self.src)["real_g3"], "STOP_UNAVAILABLE")

    def test_37_windows_vfs_predelegation_fixture_is_scoped_and_inventory_reviewed(self):
        p = "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"
        source = self.src[p]
        self.assertEqual(counts(source), (25, 0, 0, 0, 0, 26, 0))
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_sqlite_vfs_preopen_tests;",
                      self.src["src-tauri/src/lib.rs"])
        for required in ("sqlite3_vfs_register", "sqlite3_vfs_unregister", "fixture_xopen",
                         "SQLITE_OPEN_MAIN_DB", "SQLITE_OPEN_MAIN_JOURNAL", "makeDflt=0",
                         "Connection::open_with_flags_and_vfs", "create_new(true)",
                         "SQLITE_CANTOPEN"):
            self.assertIn(required, source)
        for forbidden in ("#[tauri::command]", "database::open_database(",
                          "com.fabulaxiom.greenfield.v1", "M:\\\\Fabulaxiom",
                          "run_migrations(", "SQLITE_FCNTL_WIN32_SET_HANDLE"):
            self.assertNotIn(forbidden, source)
        self.assertEqual(repository_inventory()["writer_absence"], "NOT_PROVEN")

    def test_38_predelegation_fileid128_is_still_non_atomic_test_only(self):
        source = self.src["src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"]
        for signal in ("GetFileInformationByHandleEx", "SQLITE_FCNTL_WIN32_GET_HANDLE",
                       "FileIdPrecheckPlan", "move_original_to", "fs::rename",
                       "swaps_after_precheck", "NOT an atomic authorization",
                       "m32_vfs_fixture_fileid128_precheck_accepts_stable_disposable_identity",
                       "m32_vfs_fixture_fileid128_precheck_refuses_already_replaced_name",
                       "m32_vfs_fixture_fileid128_precheck_then_internal_name_swap_is_not_atomic"):
            self.assertIn(signal, source)
        self.assertGreaterEqual(source.count("#[test]"), 6)
        self.assertEqual(counts(source), (25, 0, 0, 0, 0, 26, 0))
        self.assertNotIn("#[tauri::command]", source)
        self.assertNotIn("run_migrations(", source)
        self.assertEqual(repository_inventory()["real_g3"], "STOP_UNAVAILABLE")

    def test_39_windows_vfs_wal_and_shm_are_distinct_observation_surfaces(self):
        source = self.src["src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"]
        for signal in ("SQLITE_OPEN_WAL", "deny_wal", "wal_refusals",
                       "wal_delegations", "shm_named_xopens", "-shm", "xShmMap",
                       "m32_vfs_fixture_wal_refusal_precedes_named_default_open",
                       "m32_vfs_fixture_wal_xopen_does_not_cover_shm_mapping"):
            self.assertIn(signal, source)
        self.assertGreaterEqual(source.count("#[test]"), 8)
        self.assertEqual(counts(source), (25, 0, 0, 0, 0, 26, 0))
        for forbidden in ("#[tauri::command]", "run_migrations(", "SQLITE_FCNTL_WIN32_SET_HANDLE"):
            self.assertNotIn(forbidden, source)
        self.assertEqual(repository_inventory()["writer_absence"], "NOT_PROVEN")

    def test_40_shm_io_methods_wrapper_is_disposable_and_fail_closed(self):
        source = self.src["src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"]
        for signal in ("FixtureMainFileTail", "wrap_main_shm", "file_tail_offset",
                       "default_file_size.div_ceil", "fixture_xshm_map", "SQLITE_IOERR_SHMMAP",
                       "shm_map_refusals", "shm_map_delegations",
                       "m32_vfs_fixture_wrapped_shm_map_refuses_before_default_mapping",
                       "m32_vfs_fixture_wrapped_shm_map_delegates_disposable_wal"):
            self.assertIn(signal, source)
        self.assertGreaterEqual(source.count("#[test]"), 18)
        self.assertEqual(counts(source), (25, 0, 0, 0, 0, 26, 0))
        for forbidden in ("#[tauri::command]", "run_migrations(", "SQLITE_FCNTL_WIN32_SET_HANDLE"):
            self.assertNotIn(forbidden, source)
        self.assertEqual(repository_inventory()["real_g3"], "STOP_UNAVAILABLE")

    def test_41_v7_writer_preparation_has_no_runtime_admission_or_opener(self):
        p = "src-tauri/src/m32_v7_writer_service.rs"
        source = self.src[p]
        self.assertEqual(counts(source), (2, 0, 1, 0, 1, 0, 0))
        for signal in ("V7WriterAdmission", "_sealed", "fictional_ram_only",
                       "PreparedV7Writer", "SyncSender<Command>", "sync_channel(QUEUE_CAPACITY)",
                       "TransactionBehavior::Immediate", "set_transaction_behavior",
                       "try_send", "busy_timeout", "fn stop_worker",
                       "m32_v7_writer_prepared_two_clients_one_connection_ordered",
                       "m32_v7_writer_prepared_shutdown_revokes_cloned_clients"):
            self.assertIn(signal, source)
        for forbidden in ("#[tauri::command]", "Connection::open(",
                          "Connection::open_with_flags", "database::open_database(",
                          "SQLITE_FCNTL_WIN32_SET_HANDLE", "migration_007", "&Path"):
            self.assertNotIn(forbidden, source)
        lib = self.src["src-tauri/src/lib.rs"]
        self.assertIn("mod m32_v7_writer_service;", lib)
        self.assertNotIn("m32_v7_writer_service::", lib)
        self.assertEqual(repository_inventory()["writer_absence"], "NOT_PROVEN")


    def test_42_d3b5_disposable_phase_matrix_is_exactly_one_reviewed_test_only_open(self):
        p = "src-tauri/src/m32_d3b5_phase_matrix_tests.rs"
        source = self.src[p]
        self.assertEqual(EXPECTED[p], (1, 0, 0, 0, 0, 1, 0))
        self.assertEqual(counts(source), (1, 0, 0, 0, 0, 1, 0))
        self.assertEqual(source.count("#[test]"), 4)
        self.assertIn("TerminateProcess(GetCurrentProcess()", source)
        self.assertIn("RECOVERY_REQUIRED_NOT_AUTHORIZED", source)
        self.assertIn("create_new(true)", source)
        self.assertIn("std::env::temp_dir()", source)
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_d3b5_phase_matrix_tests;",
                      self.src["src-tauri/src/lib.rs"])
        for forbidden in ("#[tauri::command]", "app_local_data_dir()",
                          "database::open_database(", "SQLITE_OPEN_CREATE",
                          "run_migrations(", "VACUUM INTO", "ATTACH DATABASE"):
            self.assertNotIn(forbidden, source)
        self.assertFalse(audit_inventory(self.src)["real_g3_authorized"])


    def test_43_p1_integrated_prefix_is_windows_only_and_never_opens_sqlite(self):
        p = "src-tauri/src/m32_p1_integrated_prefix_tests.rs"
        source = self.src[p]
        self.assertEqual(counts(source), (0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(source.count("#[test]"), 5)
        self.assertIn("GetFileInformationByHandleEx", source)
        self.assertIn("CreateMutexW", source)
        self.assertIn("create_new(true)", source)
        self.assertIn("R2AncestorsNotPinned", source)
        self.assertIn("R7PredecessorUnknown", source)
        self.assertIn("#[cfg(all(test, windows))]\\nmod m32_p1_integrated_prefix_tests;".replace("\\n", "\n"),
                      self.src["src-tauri/src/lib.rs"])
        for forbidden in ("#[tauri::command]", "Connection::open(", "Connection::open_with_flags(",
                          "Connection::open_with_flags_and_vfs(", "database::open_database(",
                          "sqlite3_open", "migration_007", "SQLITE_OPEN_CREATE",
                          "app_local_data_dir()", "tauri::State"):
            self.assertNotIn(forbidden, source)
        self.assertFalse(audit_inventory(self.src)["real_g3_authorized"])


    def test_44_r2_held_parent_chain_stops_before_sqlite_and_is_not_runtime(self):
        p = "src-tauri/src/m32_r2_held_parent_chain_tests.rs"
        src = self.src[p]
        self.assertEqual(counts(src), (0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(src.count("#[test]"), 4)
        for needle in ("FILE_FLAG_BACKUP_SEMANTICS", "FILE_FLAG_OPEN_REPARSE_POINT",
                       "FILE_READ_ATTRIBUTES", "GetFileInformationByHandleEx",
                       "CreateMutexW", "FILE_SHARE_READ | FILE_SHARE_WRITE",
                       "R4ShmMappingUnproven", "PinnedChain", "sidecars_absent",
                       "create_new(true)", "m32_p1_r2_parent_rename_while_held_is_denied_or_detected",
                       "m32_p1_r2_parent_pins_do_not_authenticate_replaced_main_name"):
            self.assertIn(needle, src)
        for forbidden in ("#[tauri::command]", "Connection::open(", "Connection::open_with_flags",
                          "database::open_database(", "sqlite3_open", "SQLITE_OPEN_CREATE",
                          "migration_007", "app_local_data_dir()", "tauri::State"):
            self.assertNotIn(forbidden, src)
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_r2_held_parent_chain_tests;",
                      self.src["src-tauri/src/lib.rs"])
        self.assertFalse(repository_inventory()["real_g3_authorized"])


    def test_45_r23_exactly_one_windows_test_only_sqlite_opener_is_reviewed(self):
        p = "src-tauri/src/m32_r23_sqlite_handle_boundary_tests.rs"
        source = self.src[p]
        self.assertEqual(counts(source), (1, 0, 0, 0, 0, 1, 0))
        self.assertEqual(EXPECTED[p], (1, 0, 0, 0, 0, 1, 0))
        self.assertEqual(source.count("#[test]"), 10)
        for needle in ("GetFileInformationByHandleEx", "SQLITE_FCNTL_WIN32_GET_HANDLE",
                       "FILE_ID_INFO", "SqliteHandleUnavailable",
                       "R4MappingUnproven", "swap_after_precheck", "create_new(true)",
                       "FILE_ID_INFO", "UnknownSidecar", "Pins",
                       "m32_r23_controlled_swap_after_precheck_vetoes_real_sqlite_handle",
                       "m32_r3_held_main_without_delete_share_refuses_rename_before_sqlite_open",
                       "m32_r3_held_main_without_delete_share_survives_sqlite_xopen_but_stops_at_r4",
                       "m32_r3_child_rename_probe_only_fresh_disposable_main",
                       "m32_r3_other_process_rename_is_refused_before_and_during_sqlite_xopen",
                       "m32_r3_reopenfile_preserves_live_disposable_main_identity_without_path_lookup",
                       "m32_r3_reopenfile_binds_original_file_even_after_name_replacement",
                       ".share_mode(SHARE_READ | SHARE_WRITE)"):
            self.assertIn(needle, source)
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_r23_sqlite_handle_boundary_tests;",
                      self.src["src-tauri/src/lib.rs"])
        for forbidden in ("#[tauri::command]", "database::open_database(",
                          "run_migrations(", "SQLITE_OPEN_CREATE", "ATTACH DATABASE",
                          "VACUUM INTO", "app_local_data_dir()", "V7WriterAdmission {"):
            self.assertNotIn(forbidden, source)
        self.assertFalse(repository_inventory()["real_g3_authorized"])


    def test_46_r4_exclusive_before_wal_is_disposable_only_and_does_not_admit_writer(self):
        p = "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"
        source = self.src[p]
        self.assertEqual(counts(source), (25, 0, 0, 0, 0, 26, 0))
        for name in (
            "m32_r4_exclusive_before_wal_avoids_every_wrapped_shm_callback",
            "m32_r4_exclusive_before_wal_succeeds_with_shm_map_veto_armed",
            "m32_r4_exclusive_after_wal_does_not_undo_existing_shm_mapping",
        ):
            self.assertIn("fn " + name + "(", source)
        self.assertIn("PRAGMA locking_mode=EXCLUSIVE", source)
        self.assertIn("PRAGMA journal_mode=WAL", source)
        self.assertIn("d3a_shm_unmap_delegations", source)
        self.assertIn("RegisteredFixtureVfs::with_shm_policy(true)", source)
        # Historical VFS fixtures already contain an OPEN_CREATE policy token.
        # Scope new negative assertions to the added R4 module only, without
        # weakening the existing whole-tree/old-module inventory checks.
        new_r4 = source.split("// R4 / P1 decision probe", 1)[1].split("// R3 preopened HANDLE xOpen veto", 1)[0]
        for forbidden in (
            "#[tauri::command]", "database::open_database(",
            "run_migrations(", "SQLITE_OPEN_CREATE",
            "V7WriterAdmission {", "M:\\\\Fabulaxiom",
        ):
            self.assertNotIn(forbidden, new_r4)
        self.assertEqual(repository_inventory()["real_g3"], "STOP_UNAVAILABLE")


    def test_47_r4_p1_no_second_reader_and_sticky_exclusive_is_disposable_only(self):
        src = self.src["src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"]
        self.assertEqual(counts(src), (25, 0, 0, 0, 0, 26, 0))
        r4 = src.split("// R4 / P1 decision probe", 1)[1].split("// R3 preopened HANDLE xOpen veto", 1)[0]
        for name in (
            "m32_r4_exclusive_owner_refuses_second_sqlite_reader_without_ipc",
            "m32_r4_exclusive_wal_owner_policy_refuses_normal_downgrade",
        ):
            self.assertIn("fn " + name + "(", r4)
        self.assertIn("SQLITE_OPEN_READ_ONLY", r4)
        self.assertIn("ErrorCode::DatabaseBusy", r4)
        self.assertIn("R4OwnerRequest::DowngradeLockingToNormal", r4)
        self.assertIn("r4_fixture_owner_execute", r4)
        self.assertNotIn('"PRAGMA locking_mode=NORMAL"', r4)
        self.assertEqual(r4.count("#[test]"), 5)
        self.assertNotIn("SQLITE_OPEN_CREATE", r4)
        self.assertNotIn("#[tauri::command]", r4)
        self.assertEqual(repository_inventory()["real_g3"], "STOP_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
