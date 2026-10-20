"""Adversarial synthetic-only rejection matrix for G2-A writer evidence."""
from dataclasses import replace, fields
import unittest

from m32_g2a_writer_gap_model import SourceOnlyEvidence, evaluate

class WriterGapRejectTests(unittest.TestCase):
    def veto(self, e):
        result=evaluate(e)
        self.assertEqual(result["process_writer_absence"],"NOT_PROVEN")
        self.assertEqual(result["real_g3"],"STOP_UNAVAILABLE")
        self.assertEqual(result["downstream"],"NOT_AUTHORIZED")
        self.assertFalse(result["real_g3_authorized"])
        self.assertFalse(result["source_identity_authenticated"])
        self.assertFalse(result["trusted_nonmigrating_owner_established"])
        self.assertFalse(result["cold_quiescence_and_journals_established"])

    def test_01_default_refuses(self):
        self.veto(SourceOnlyEvidence())

    def test_02_metadata_pass_is_not_writer_absence(self):
        self.veto(SourceOnlyEvidence(g2a_metadata_pass=True))

    def test_03_process_name_inventory_is_not_writer_proof(self):
        self.veto(SourceOnlyEvidence(g2a_metadata_pass=True,process_names_absent=True))

    def test_04_no_sidecars_not_writer_proof(self):
        self.veto(SourceOnlyEvidence(no_sidecars_seen=True))

    def test_05_hash_stability_not_writer_proof(self):
        self.veto(SourceOnlyEvidence(hashes_stable=True))

    def test_06_exclusive_handle_toy_not_proven(self):
        self.veto(SourceOnlyEvidence(exclusive_handle_toy=True))

    def test_07_file_id_toy_not_proven(self):
        self.veto(SourceOnlyEvidence(file_identity_toy=True))

    def test_08_preopened_owner_toy_not_real_owner(self):
        self.veto(SourceOnlyEvidence(preopened_owner_toy=True))

    def test_09_all_fictional_flags_still_never_real_g3(self):
        allflags={f.name: True for f in fields(SourceOnlyEvidence)}
        self.veto(SourceOnlyEvidence(**allflags))

    def test_10_each_single_flag_never_promotes(self):
        for f in fields(SourceOnlyEvidence):
            self.veto(replace(SourceOnlyEvidence(),**{f.name:True}))

    def test_11_stop_on_untrusted_dict(self):
        with self.assertRaises(TypeError):
            evaluate({"all_fictional_checks_true":True})

    def test_12_stop_on_integer_masquerading_as_bool(self):
        with self.assertRaises(TypeError):
            evaluate(SourceOnlyEvidence(g2a_metadata_pass=1))

    def test_13_no_permission_even_if_all_true(self):
        allflags={f.name: True for f in fields(SourceOnlyEvidence)}
        x=evaluate(SourceOnlyEvidence(**allflags))
        self.assertEqual(x["operator_permission"],"NEW_EXPLICIT_APPROVAL_REQUIRED")
        self.assertEqual(x["historic_custody"],"PENDING_EXTERNAL_ATTESTATION(21/3/2)")
        self.assertEqual(x["prospective_baseline"],"NOT_STARTED")

if __name__ == "__main__":
    unittest.main()
