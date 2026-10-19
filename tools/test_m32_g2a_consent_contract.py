"""Fail-closed adversarial checks on a NON EXECUTABLE G2-A review proposal."""
from copy import deepcopy
import unittest

from m32_g2a_consent_contract import (
    PacketStop, OBSERVATIONS, validate_packet, load_packet,
)


class G2AProposalOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_packet()

    def veto(self, mutate):
        s = deepcopy(self.source)
        mutate(s)
        with self.assertRaises(PacketStop):
            validate_packet(s)

    def test_01_proposal_is_inert_and_not_operator_approved(self):
        result = validate_packet(self.source)
        self.assertEqual(result["g2a_execution"], "NOT_AUTHORIZED")

    def test_02_all_five_G2_A_observation_names_are_bounded(self):
        actual = self.source["proposed_observations"]
        self.assertEqual({x["id"]: x["scope"] for x in actual}, OBSERVATIONS)

    def test_03_converting_proposal_to_script_is_denied(self):
        self.veto(lambda s: s["packet"].update(commands_included=True))

    def test_04_script_digest_is_not_owner_consent(self):
        self.veto(lambda s: s["packet"].update(script_sha256="f"*64))

    def test_05_operator_path_in_public_packet_is_denied(self):
        self.veto(lambda s: s["packet"].update(operator_paths_included=True))

    def test_06_operator_approval_cannot_be_inferred(self):
        self.veto(lambda s: s["packet"].update(operator_approval="GRANTED"))

    def test_07_automatic_execution_remains_forbidden(self):
        self.veto(lambda s: s["packet"].update(auto_execution=True))

    def test_08_scheduled_execution_remains_forbidden(self):
        self.veto(lambda s: s["packet"].update(auto_scheduling=True))

    def test_09_exact_command_requires_a_later_separate_review(self):
        self.veto(lambda s: s["packet"].update(requires_distinct_reviewed_command=False))

    def test_10_g2a_result_starts_unassessed(self):
        self.veto(lambda s: s["results"].update(g2a_runtime="PASS"))

    def test_11_g2b_inventory_needs_another_gate(self):
        self.veto(lambda s: s["results"].update(g2b="AUTHORIZED"))

    def test_12_g3_capture_cannot_follow_packet_ci(self):
        self.veto(lambda s: s["results"].update(g3="AUTHORIZED"))

    def test_13_original_sqlite_open_is_prohibited(self):
        self.veto(lambda s: s["effect_contract"].update(protected_sqlite_open="READ_ONLY"))

    def test_14_process_stop_is_forbidden(self):
        self.veto(lambda s: s["effect_contract"].update(process_stop="ALLOWED"))

    def test_15_windows_elevation_is_forbidden(self):
        self.veto(lambda s: s["effect_contract"].update(elevation="ALLOWED"))

    def test_16_private_acls_are_not_observed_in_g2a(self):
        self.veto(lambda s: s["effect_contract"].update(acl_read="ALLOWED"))

    def test_17_operator_machine_network_calls_require_review(self):
        self.veto(lambda s: s["effect_contract"].update(remote_network_on_operator_machine="ALLOWED"))

    def test_18_remove_any_stop_makes_packet_invalid(self):
        self.veto(lambda s: s["abort_policy"].pop("unexpected_integrity"))

    def test_19_any_unknown_or_duplicate_observation_is_denied(self):
        self.veto(lambda s: s["proposed_observations"][4].update(id="clock_context"))

    def test_20_no_executable_command_in_purpose(self):
        self.veto(lambda s: s["proposed_observations"][0].update(purpose="powershell.exe -command fake"))

    def test_21_declared_path_to_private_data_is_unreviewed(self):
        self.veto(lambda s: s.update(operator_data_path="C:\\placeholder\\no-real-path"))

    def test_22_solo_operator_not_independent_attestation(self):
        self.veto(lambda s: s["authority"].update(historical="VERIFIED"))

    def test_23_tauri_runtime_still_untested(self):
        self.veto(lambda s: s["authority"].update(tauri_runtime="PASS"))

    def test_24_operator_signature_is_not_a_public_json_field(self):
        self.veto(lambda s: s["operator_fields"].update(authorized_run_id="fake"))

if __name__ == "__main__":
    unittest.main()
