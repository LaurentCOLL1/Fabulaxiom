"""M3.2 G3: toy-only negative proof of endpoint/path ABA security gap."""
import os
from pathlib import Path
import tempfile
import unittest

from m3_2_g3_win_single_handle_toy import TOY_PREFIX, create_fictional_toy
from m3_2_g3_namespace_aba_toy import (
    EndpointEvidence, TransientToyVeto, checkpoint_only_verdict,
    require_real_g3_authority, toy_transient_rename, toy_transient_sidecar
)


class EndpointPolicyTests(unittest.TestCase):
    def test_equal_endpoints_are_not_a_real_proof(self):
        equal = EndpointEvidence((42, 17), (42, 17))
        self.assertEqual(checkpoint_only_verdict(equal), "ENDPOINT_EQUAL_TRANSIENT_UNPROVEN")

    def test_endpoint_identity_difference_is_a_veto(self):
        different = EndpointEvidence((42, 17), (42, 19))
        self.assertEqual(checkpoint_only_verdict(different), "VETO_OBSERVED_IDENTITY_MISMATCH")

    def test_missing_file_identity_is_a_veto(self):
        self.assertEqual(
            checkpoint_only_verdict(EndpointEvidence((), (42, 17))),
            "VETO_OBSERVED_IDENTITY_MISMATCH"
        )

    def test_invisible_aba_and_stable_history_have_same_endpoints(self):
        stable = [(42, 17), (42, 17)]
        transient = [(42, 17), (77, 999), (42, 17)]
        self.assertEqual(
            EndpointEvidence(stable[0], stable[-1]),
            EndpointEvidence(transient[0], transient[-1])
        )
        self.assertEqual(
            checkpoint_only_verdict(EndpointEvidence(stable[0], stable[-1])),
            "ENDPOINT_EQUAL_TRANSIENT_UNPROVEN"
        )

    def test_toy_success_cannot_authorize_real_g3(self):
        with self.assertRaisesRegex(TransientToyVeto, "REAL_G3_NOT_AUTHORIZED"):
            require_real_g3_authority(toy_verdict="TOY_ONLY_PASS")

    def test_different_provenance_does_not_bypass_veto(self):
        for label in ("toy", "operator", "attested"):
            with self.subTest(label=label):
                with self.assertRaises(TransientToyVeto):
                    require_real_g3_authority(toy_verdict="TOY_ONLY_PASS", provenance=label)


@unittest.skipUnless(os.name == "nt", "Windows-only toy fixture")
class Win32ToyABAObservations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=TOY_PREFIX)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = create_fictional_toy(self.root, 6)

    def test_rename_and_restore_is_denied_or_endpoint_blind(self):
        before = self.source.read_bytes()
        result = toy_transient_rename(self.root, self.source)
        self.assertTrue(result["attempted"])
        self.assertEqual(result["audit_result"], "TOY_ONLY_PASS")
        self.assertFalse(result["real_g3_authorized"])
        self.assertEqual(result["endpoint_only_safety"], "UNPROVEN")
        self.assertEqual(before, self.source.read_bytes())
        self.assertTrue(result["kernel_denied"] or result["renamed"])
        if result["renamed"]:
            self.assertTrue(result["restored"])

    def test_transient_journal_is_not_observed_at_boundary(self):
        original = self.source.read_bytes()
        result = toy_transient_sidecar(self.root, self.source)
        self.assertTrue(result["journal_transient"])
        self.assertEqual(result["checkpoint_audit"], "TOY_ONLY_PASS")
        self.assertFalse(result["real_g3_authorized"])
        self.assertFalse(Path(str(self.source) + "-journal").exists())
        self.assertEqual(self.source.read_bytes(), original)

    def test_unrecognized_source_role_is_refused(self):
        with self.assertRaisesRegex(TransientToyVeto, "unrecognized"):
            toy_transient_rename(self.root, self.root / "operator.sqlite3")

    def test_attacker_detour_collision_is_refused(self):
        detour = self.root.with_name(self.root.name + "-aba-detour")
        detour.mkdir()
        self.addCleanup(lambda: detour.rmdir() if detour.exists() else None)
        with self.assertRaisesRegex(TransientToyVeto, "occupied"):
            toy_transient_rename(self.root, self.source)

    def test_existing_sidecar_is_never_replaced(self):
        journal = Path(str(self.source) + "-journal")
        journal.write_bytes(b"PREEXISTING TOY JOURNAL")
        with self.assertRaisesRegex(TransientToyVeto, "preexisting"):
            toy_transient_sidecar(self.root, self.source)
        self.assertEqual(journal.read_bytes(), b"PREEXISTING TOY JOURNAL")


if __name__ == "__main__":
    unittest.main()
