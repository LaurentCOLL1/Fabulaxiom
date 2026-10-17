"""M3.2 G3 no-I/O service design contract and current Rust code-only audit."""
from dataclasses import fields, replace
from pathlib import Path
import unittest

from m3_2_g3_owner_runtime_contract import (
    Route, HypotheticalEvidence, review, current_rust_owner_status,
)

REPO = Path(__file__).resolve().parents[1]


class OwnerRuntimePolicyTests(unittest.TestCase):
    def setUp(self):
        self.all_true = HypotheticalEvidence(
            **{item.name: True for item in fields(HypotheticalEvidence)}
        )

    def test_every_default_route_denies_real_g3(self):
        for route in Route:
            with self.subTest(route=route):
                self.assertFalse(review(route, HypotheticalEvidence()).real_g3_authorized)

    def test_known_runtime_owner_unavailable(self):
        report = current_rust_owner_status()
        self.assertEqual(report.status, "STOP_UNPROVEN_CONDITIONS")
        self.assertIn("owner_connection_already_exists", report.missing)

    def test_hypothetical_all_true_is_not_authority(self):
        for route in (Route.EXISTING_OWNER_SERVICE, Route.VERIFIED_COLD_CUSTODY):
            with self.subTest(route=route):
                report = review(route, self.all_true)
                self.assertEqual(report.status, "HYPOTHETICAL_REVIEW_ONLY")
                self.assertFalse(report.real_g3_authorized)

    def test_existing_effectful_routes_always_veto_even_all_true(self):
        forbidden = (
            Route.CURRENT_DATABASE_STATUS,
            Route.CURRENT_APP_BACKUP,
            Route.CURRENT_APP_RESTORE,
            Route.RAW_LIVE_COPY,
        )
        for route in forbidden:
            with self.subTest(route=route):
                self.assertEqual(
                    review(route, self.all_true).status,
                    "VETO_EXISTING_EFFECTFUL_OR_UNSAFE_ROUTE",
                )

    def test_existing_owner_requires_preexisting_connection(self):
        report = review(Route.EXISTING_OWNER_SERVICE,
                        replace(self.all_true, owner_connection_already_exists=False))
        self.assertIn("owner_connection_already_exists", report.missing)

    def test_existing_owner_requires_provenance_not_pathname(self):
        report = review(Route.EXISTING_OWNER_SERVICE,
                        replace(self.all_true, source_binding_independent_of_pathname=False))
        self.assertIn("source_binding_independent_of_pathname", report.missing)

    def test_reopening_original_for_backup_is_veto(self):
        report = review(Route.EXISTING_OWNER_SERVICE,
                        replace(self.all_true, no_new_original_open=False))
        self.assertIn("no_new_original_open", report.missing)

    def test_migration_or_recovery_is_veto(self):
        report = review(Route.EXISTING_OWNER_SERVICE,
                        replace(self.all_true, no_migrations_or_recovery_on_original=False))
        self.assertIn("no_migrations_or_recovery_on_original", report.missing)

    def test_owner_lifetime_and_serialization_both_required(self):
        for name in ("owner_session_lifetime_continuous", "owner_access_serialized",
                     "revocation_prevents_reopen"):
            with self.subTest(name=name):
                report = review(Route.EXISTING_OWNER_SERVICE,
                                replace(self.all_true, **{name: False}))
                self.assertIn(name, report.missing)

    def test_cold_route_does_not_claim_a_preopened_owner(self):
        claims = replace(
            self.all_true,
            owner_connection_already_exists=False,
            owner_is_bound_to_original=False,
            no_new_original_open=False,
        )
        report = review(Route.VERIFIED_COLD_CUSTODY, claims)
        self.assertEqual(report.status, "HYPOTHETICAL_REVIEW_ONLY")
        self.assertFalse(report.real_g3_authorized)

    def test_cold_copy_requires_all_writers_quiescent(self):
        report = review(Route.VERIFIED_COLD_CUSTODY,
                        replace(self.all_true, all_writers_quiescent=False))
        self.assertIn("all_writers_quiescent", report.missing)

    def test_cold_copy_requires_authenticated_ancestors(self):
        report = review(Route.VERIFIED_COLD_CUSTODY,
                        replace(self.all_true, original_and_ancestors_authenticated=False))
        self.assertIn("original_and_ancestors_authenticated", report.missing)

    def test_cold_copy_requires_resolved_journals(self):
        report = review(Route.VERIFIED_COLD_CUSTODY,
                        replace(self.all_true,
                                journals_resolved_without_original_mutation=False))
        self.assertIn("journals_resolved_without_original_mutation", report.missing)

    def test_atomic_new_only_private_output_is_required(self):
        for route in (Route.EXISTING_OWNER_SERVICE, Route.VERIFIED_COLD_CUSTODY):
            self.assertIn("new_only_private_output_sealed",
                          review(route, replace(self.all_true,
                                new_only_private_output_sealed=False)).missing)

    def test_third_location_restore_is_required(self):
        report = review(Route.EXISTING_OWNER_SERVICE,
                        replace(self.all_true, independent_third_location_restore=False))
        self.assertIn("independent_third_location_restore", report.missing)

    def test_separate_operator_consent_cannot_be_assumed(self):
        report = review(Route.EXISTING_OWNER_SERVICE,
                        replace(self.all_true, operator_specific_consent=False))
        self.assertIn("operator_specific_consent", report.missing)

    def test_untyped_route_fails(self):
        with self.assertRaises(TypeError):
            review("EXISTING_OWNER_SERVICE", self.all_true)

    def test_no_path_or_credentials_inputs_in_policy(self):
        names = tuple(x.name for x in fields(HypotheticalEvidence))
        # A *description* of pathname trust is not an input filesystem path.
        self.assertFalse(any(
            name in ("path", "password", "token", "secret")
            or name.endswith(("_path", "_password", "_token", "_secret"))
            for name in names
        ))


class ExistingRustSourceCodeAudit(unittest.TestCase):
    """These inspect PUBLIC REPO SOURCE CODE ONLY, not any runtime database."""

    @staticmethod
    def read(path):
        return (REPO / path).read_text(encoding="utf-8")

    def test_database_open_runs_migrations(self):
        source = self.read("src-tauri/src/database.rs")
        fn = source.split("pub fn open_database(", 1)[1].split("pub fn ", 1)[0]
        self.assertIn("run_migrations(&mut connection)?", fn)

    def test_existing_backup_reopens_via_migration_path(self):
        source = self.read("src-tauri/src/backup.rs")
        fn = source.split("pub fn create_backup(", 1)[1].split("pub fn ", 1)[0]
        self.assertIn("database::open_database", fn)
        self.assertIn("vacuum_copy", fn)

    def test_current_backup_uses_vacuum_into(self):
        source = self.read("src-tauri/src/backup.rs")
        self.assertIn("VACUUM INTO", source)

    def test_toy_feature_not_enabled_in_default_builds(self):
        cargo = self.read("src-tauri/Cargo.toml")
        self.assertIn("default = []", cargo)
        self.assertIn('m32-g3-owned-ram-toy = ["rusqlite/backup"]', cargo)

    def test_toy_feature_compile_fails_outside_unit_tests(self):
        lib = self.read("src-tauri/src/lib.rs")
        self.assertIn('feature = "m32-g3-owned-ram-toy", not(test)', lib)
        self.assertIn("compile_error!", lib)


if __name__ == "__main__":
    unittest.main()
