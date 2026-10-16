"""Deterministic G3 source strategy policy; NO REAL SQLite OR OPERATOR PATHS."""
from dataclasses import fields, replace
import subprocess
import sys
import unittest

from m3_2_g3_source_strategy_policy import (
    Strategy, Evidence, classify, preferred_strategy,
)


class G3PolicyTests(unittest.TestCase):
    def test_default_stop(self):
        for strategy in Strategy:
            with self.subTest(strategy=strategy.value):
                self.assertFalse(classify(strategy, Evidence()).real_g3_authorized)

    def test_missing_app_owner_never_offers_review(self):
        result = classify(Strategy.APP_OWNED_BACKUP, Evidence())
        self.assertFalse(result.design_review_candidate)
        self.assertIn("existing_trusted_owner_connection", result.unmet_conditions)

    def test_new_path_open_not_substitute_for_existing_connection(self):
        toy = Evidence(existing_trusted_owner_connection=True, no_new_source_open=False)
        result = classify(Strategy.APP_OWNED_BACKUP, toy)
        self.assertIn("no_new_source_open", result.unmet_conditions)

    def test_auto_migration_is_veto(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        changed = replace(all_true, no_automatic_migration=False)
        self.assertIn("no_automatic_migration",
                      classify(Strategy.APP_OWNED_BACKUP, changed).unmet_conditions)

    def test_unresolved_journal_is_veto(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        for mode in (Strategy.APP_OWNED_BACKUP, Strategy.VERIFIED_COLD_SNAPSHOT):
            with self.subTest(mode=mode.value):
                result = classify(mode, replace(all_true, journal_state_resolved=False))
                self.assertFalse(result.design_review_candidate)

    def test_source_binding_absent_is_veto(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        self.assertFalse(classify(Strategy.APP_OWNED_BACKUP,
                                  replace(all_true, source_binding_attested=False)
                                  ).design_review_candidate)

    def test_cold_requires_quiescence(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.VERIFIED_COLD_SNAPSHOT,
                          replace(all_true, source_quiescence_attested=False))
        self.assertIn("source_quiescence_attested", result.unmet_conditions)

    def test_cold_requires_full_path_identity(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.VERIFIED_COLD_SNAPSHOT,
                          replace(all_true, ancestors_identity_attested=False))
        self.assertIn("ancestors_identity_attested", result.unmet_conditions)

    def test_cold_requires_held_source_identity(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.VERIFIED_COLD_SNAPSHOT,
                          replace(all_true, source_handle_identity_attested=False))
        self.assertIn("source_handle_identity_attested", result.unmet_conditions)

    def test_raw_live_copy_always_veto_even_all_true(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.RAW_LIVE_COPY, all_true)
        self.assertFalse(result.design_review_candidate)
        self.assertEqual(result.disposition, "VETO_NO_REAL_SOURCE_ACCESS")

    def test_mode_ro_not_safe_proof_even_all_true(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.READONLY_PATH_OPEN, all_true)
        self.assertEqual(result.disposition, "VETO_NO_REAL_SOURCE_ACCESS")

    def test_all_true_is_only_design_review_never_real_g3(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        for strategy in (Strategy.APP_OWNED_BACKUP, Strategy.VERIFIED_COLD_SNAPSHOT):
            with self.subTest(strategy=strategy.value):
                result = classify(strategy, all_true)
                self.assertTrue(result.design_review_candidate)
                self.assertFalse(result.real_g3_authorized)
                self.assertEqual(result.disposition, "SYNTHETIC_DESIGN_REVIEW_ONLY")

    def test_explicit_operator_permission_claim_does_not_authorize(self):
        claim = Evidence(explicit_operator_permission=True)
        self.assertFalse(classify(Strategy.APP_OWNED_BACKUP, claim).real_g3_authorized)

    def test_destination_collision_plan_veto(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.APP_OWNED_BACKUP,
                          replace(all_true, new_only_destination_plan=False))
        self.assertIn("new_only_destination_plan", result.unmet_conditions)

    def test_private_destination_plan_required(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.VERIFIED_COLD_SNAPSHOT,
                          replace(all_true, private_destination_plan=False))
        self.assertIn("private_destination_plan", result.unmet_conditions)

    def test_restore_plan_required(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.APP_OWNED_BACKUP,
                          replace(all_true, isolated_restoration_plan=False))
        self.assertIn("isolated_restoration_plan", result.unmet_conditions)

    def test_memory_budget_plan_required(self):
        all_true = Evidence(**{f.name: True for f in fields(Evidence)})
        result = classify(Strategy.APP_OWNED_BACKUP,
                          replace(all_true, memory_capacity_plan=False))
        self.assertIn("memory_capacity_plan", result.unmet_conditions)

    def test_no_strategy_when_app_off_and_no_quiescence(self):
        self.assertEqual(
            preferred_strategy(app_connection_preexists=False,
                               source_quiescence_proven=False),
            "NO_ELIGIBLE_STRATEGY_STOP",
        )

    def test_owned_preferred_when_connection_available(self):
        self.assertEqual(
            preferred_strategy(app_connection_preexists=True,
                               source_quiescence_proven=True),
            "APP_OWNED_BACKUP",
        )

    def test_cold_fallback_only_with_proven_quiescence(self):
        self.assertEqual(
            preferred_strategy(app_connection_preexists=False,
                               source_quiescence_proven=True),
            "VERIFIED_COLD_SNAPSHOT",
        )

    def test_bad_type_fails_closed(self):
        with self.assertRaises(TypeError):
            classify("APP_OWNED_BACKUP", Evidence())

    def test_evidence_fields_are_not_effectful(self):
        self.assertTrue(all(f.type is not None for f in fields(Evidence)))
        self.assertNotIn("path", tuple(f.name for f in fields(Evidence)))

    def test_cli_accepts_self_test_only(self):
        # The self test itself never touches SQLite or operator paths.
        from m3_2_g3_source_strategy_policy import main
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
