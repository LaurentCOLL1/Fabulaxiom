"""Synthetic adversarial process trees from G2-A, no Windows interrogation."""
import unittest
from m32_g2a_pid_zero_model import classify, LineageStop


def sample():
    # Invented process IDs, not any actual operator's PIDs or Windows paths.
    return [
        {"pid": 100, "parent": 1, "name": "SearchHost.exe", "created": 10},
        {"pid": 110, "parent": 100, "name": "msedgewebview2.exe", "created": 11},
        {"pid": 111, "parent": 110, "name": "msedgewebview2.exe", "created": 12},
        {"pid": 112, "parent": 110, "name": "msedgewebview2.exe", "created": 13},
        {"pid": 113, "parent": 110, "name": "msedgewebview2.exe", "created": 14},
        {"pid": 114, "parent": 110, "name": "msedgewebview2.exe", "created": 15},
        {"pid": 115, "parent": 110, "name": "msedgewebview2.exe", "created": 16},
    ]


class IdlePidZeroLineageFixtures(unittest.TestCase):
    def veto(self, data, pids):
        with self.assertRaises(LineageStop):
            classify(data, pids)

    def test_01_searchhost_six_webview_children_can_pass_metadata_only(self):
        r = classify(sample(), [110,111,112,113,114,115])
        self.assertEqual(r["searchhost_descendant_count"], 6)
        self.assertFalse(r["owner_authenticated"])
        self.assertFalse(r["sqlite_writer_absent_proven"])

    def test_02_webview_count_can_be_zero(self):
        self.assertEqual(classify([sample()[0]], [])["searchhost_descendant_count"], 0)

    def test_03_fabulaxiom_process_must_stop(self):
        v=sample(); v.append({"pid":200,"parent":1,"name":"Fabulaxiom.exe","created":5})
        self.veto(v,[110,111,112,113,114,115])

    def test_04_ollama_process_must_stop(self):
        v=sample(); v.append({"pid":201,"parent":1,"name":"ollama.exe","created":5})
        self.veto(v,[110,111,112,113,114,115])

    def test_05_another_browser_owner_must_stop(self):
        v=sample(); v[0]["name"]="OtherApp.exe"
        self.veto(v,[110,111,112,113,114,115])

    def test_06_parent_pid_absent_must_stop(self):
        v=sample(); v[1]["parent"]=9999
        self.veto(v,[110,111,112,113,114,115])

    def test_07_reused_pid_with_later_parent_creation_must_stop(self):
        v=sample(); v[0]["created"]=200
        self.veto(v,[110,111,112,113,114,115])

    def test_08_missing_timestamps_must_stop(self):
        v=sample(); v[0]["created"]=None
        self.veto(v,[110,111,112,113,114,115])

    def test_09_cycle_must_stop(self):
        v=sample(); v[0]["name"]="OtherApp.exe"; v[0]["parent"]=110
        self.veto(v,[110,111,112,113,114,115])

    def test_10_second_snapshot_count_mismatch_must_stop(self):
        self.veto(sample(),[110,111])

    def test_11_second_snapshot_unknown_pid_must_stop(self):
        self.veto(sample(),[110,111,112,113,114,777])

    def test_12_duplicate_pid_must_stop(self):
        v=sample(); v[2]["pid"]=110
        self.veto(v,[110,111,112,113,114,115])

    def test_13_excessive_chain_depth_must_stop(self):
        with self.assertRaises(LineageStop):
            classify(sample(),[110,111,112,113,114,115],max_depth=1)

    def test_14_only_ancestry_not_authenticity(self):
        result=classify(sample(),[110,111,112,113,114,115])
        self.assertTrue(result["metadata_only"])
        self.assertFalse(result["owner_authenticated"])

    def test_15_valid_idle_pid_zero_excluded_from_ancestry(self):
        v=sample(); v.insert(0, {'pid':0,'parent':0,'name':'System Idle Process','created':None})
        self.assertEqual(classify(v,[110,111,112,113,114,115])['searchhost_descendant_count'],6)

    def test_16_double_pid_zero_stops(self):
        v=sample(); idle={'pid':0,'parent':0,'name':'System Idle Process','created':None}
        self.veto([idle,idle]+v,[110,111,112,113,114,115])

    def test_17_wrong_pid_zero_name_stops(self):
        v=sample(); v.append({'pid':0,'parent':0,'name':'SearchHost.exe','created':None})
        self.veto(v,[110,111,112,113,114,115])

    def test_18_negative_pid_stops(self):
        v=sample(); v.append({'pid':-1,'parent':0,'name':'OtherApp.exe','created':None})
        self.veto(v,[110,111,112,113,114,115])

    def test_19_webview_parent_pid_zero_stops(self):
        v=sample(); v.insert(0,{'pid':0,'parent':0,'name':'System Idle Process','created':None})
        v[2]['parent']=0
        self.veto(v,[110,111,112,113,114,115])

    def test_20_webview_itself_pid_zero_stops(self):
        v=sample(); v.append({'pid':0,'parent':0,'name':'msedgewebview2.exe','created':None})
        self.veto(v,[110,111,112,113,114,115])

    def test_21_bool_pid_is_not_real_integer(self):
        v=sample(); v.append({'pid':False,'parent':0,'name':'System Idle Process','created':None})
        self.veto(v,[110,111,112,113,114,115])

    def test_22_idle_does_not_waive_unrelated_ancestor(self):
        v=sample(); v.insert(0, {'pid':0,'parent':0,'name':'System Idle Process','created':None})
        v[1]['name']='OtherApp.exe'
        self.veto(v,[110,111,112,113,114,115])
