"""Pure source-only invariants for legacy PR #35/#215 GitHub inventory.

No network or access to operator files. The historic Git SHA overlap was
observed externally and is a dated claim, not an offline live re-fetch.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/qualification/M3_2_LEGACY_PR35_PR215_RECONCILIATION_20261110.md"
CHECKLIST = ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md"
VFS = ROOT / "src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"
LIB = ROOT / "src-tauri/src/lib.rs"
D3B = (
    "m32_d3b_child_fixture_terminate_before_sqlite_close",
    "m32_d3b_committed_wal_abandoned_mutex_refuses_unattested_reopen",
    "m32_d3b_pending_wal_vanished_mutex_still_refuses_unattested_reopen",
    "m32_d3b_busy_close_does_not_attest_restart_even_after_final_close",
)

class LegacyPRReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = REPORT.read_text(encoding="utf-8")
        cls.checklist = CHECKLIST.read_text(encoding="utf-8")
        cls.vfs = VFS.read_text(encoding="utf-8")
        cls.lib = LIB.read_text(encoding="utf-8")

    def test_01_each_path_is_accounted_for_once_per_pr_and_bucket(self):
        for pr, expected in (("pr35", (5, 11, 68)), ("pr215", (6, 17, 0))):
            seen = []
            for category, count in zip(("identical", "different", "absent"), expected):
                rx = rf"### {pr} : {category} \({count}\)\n\n(.*?)(?=\n### |\n\*Chaque ligne|\Z)"
                match = re.search(rx, self.doc, flags=re.S)
                self.assertIsNotNone(match, (pr, category))
                paths = re.findall(r"^- `([^`]+)`$", match.group(1), re.M)
                self.assertEqual(len(paths), count, (pr, category))
                seen += paths
            self.assertEqual(len(seen), sum(expected))
            self.assertEqual(len(set(seen)), len(seen))

    def test_02_test_only_d3b_refusals_still_present_and_not_runtime(self):
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_sqlite_vfs_preopen_tests;", self.lib)
        self.assertIn("mod d3b_p1_disposable_crash_refusal", self.vfs)
        for fn in D3B:
            self.assertIn(f"fn {fn}()", self.vfs)
            self.assertIn(fn, self.doc)

    def test_03_pr35_chronology_remains_cfg_test_only(self):
        self.assertIn("#[cfg(test)]\nmod m32_manual_chronology;", self.lib)
        for marker in ("src-tauri/src/m32_isolated_preflight.rs",
                       "src-tauri/src/m32_sqlite_concurrency_tests.rs",
                       "68 chemins absents"):
            self.assertIn(marker, self.doc)

    def test_04_master_checklist_not_falsely_closed(self):
        self.assertIn("- [ ] **M32-007**", self.checklist)
        self.assertNotIn("- [x] **M32-007**", self.checklist)
        tasks = re.findall(r"^- \[([ x])\] \*\*(M32-\d{3})\*\*", self.checklist, re.M)
        self.assertEqual(len(tasks), 104)
        # Fifteen scoped closures include M32-074 and M32-076 current unmounted source boundaries ONLY,
        # plus M32-003, M32-005 and M32-006 documentary scopes.
        # M32-007 and all runtime gates remain open.
        # Neither historical #35/#215 sources, Linux distribution nor R1-R9 writer are admitted.
        actual_closed = {task for state, task in tasks if state == "x"}
        self.assertEqual(actual_closed, {
            "M32-001", "M32-002", "M32-003", "M32-004", "M32-005", "M32-006", "M32-037", "M32-049",
            "M32-051", "M32-074", "M32-076", "M32-094", "M32-095", "M32-096", "M32-104",
        })
        self.assertIn("- [ ] **M32-078**", self.checklist)
        self.assertIn("AUCUNE case nouvelle clôturée", self.doc)
        for flag in ("PRODUCT_FIRST_PARALLEL_SAFETY", "IN_PROGRESS_NOT_ACCEPTED",
                     "NOT_PROVEN", "STOP_UNAVAILABLE",
                     "PENDING_EXTERNAL_ATTESTATION(21/3/2)"):
            self.assertIn(flag, self.doc)


class Pr35UnitDispositionContract(unittest.TestCase):
    """Pure review contract, never re-fetches a private tree or runs operator code."""

    @classmethod
    def setUpClass(cls):
        cls.original = REPORT.read_text(encoding="utf-8")
        cls.triage = (ROOT / "docs/qualification/M3_2_PR35_PER_PATH_DISPOSITION_20261110.md").read_text(encoding="utf-8")
        cls.master = CHECKLIST.read_text(encoding="utf-8")
        cls.entries = re.findall(
            r"^\| \`([^\`]+)\` \| \`([A-Z_]+)\` \|",
            cls.triage, re.M
        )

    def original_paths(self, group, next_group):
        section = self.original.split("### pr35 : " + group)[1]
        if next_group == "__END__":
            section = section.split("### pr215 : ")[0]
        else:
            section = section.split("### pr35 : " + next_group)[0]
        return re.findall(r"^- \`([^\`]+)\`$", section, re.M)

    def test_06_complete_84_path_matrix_without_duplicate_or_spoof(self):
        pairs = dict(self.entries)
        self.assertEqual(len(self.entries), 84)
        self.assertEqual(len(pairs), 84)
        same = self.original_paths("identical (5)", "different (11)")
        changed = self.original_paths("different (11)", "absent (68)")
        absent = self.original_paths("absent (68)", "__END__")
        self.assertEqual((len(same), len(changed), len(absent)), (5, 11, 68))
        self.assertEqual(set(pairs), set(same + changed + absent))
        for p in same:
            self.assertEqual(pairs[p], "KEEP_IDENTICAL")
        for p in changed:
            self.assertEqual(pairs[p], "REVIEW_DIVERGENCE")
        for p in absent:
            self.assertNotIn(pairs[p], ("KEEP_IDENTICAL", "REVIEW_DIVERGENCE"))

    def test_07_68_absent_paths_are_scoped_and_not_automatically_admitted(self):
        pairs = dict(self.entries)
        absent = [p for p, status in pairs.items()
                  if status not in ("KEEP_IDENTICAL", "REVIEW_DIVERGENCE")]
        self.assertEqual(len(absent), 68)
        self.assertEqual(sum(p.startswith("docs/qualification/") for p in absent), 26)
        self.assertEqual(sum(p.startswith("tools/test_") for p in absent), 20)
        self.assertEqual(sum(p.startswith("tools/") and not p.startswith("tools/test_")
                             for p in absent), 20)
        self.assertEqual(sum(p.startswith("src-tauri/") for p in absent), 2)
        self.assertEqual(pairs["src-tauri/src/m32_isolated_preflight.rs"],
                         "BLOCK_RUNTIME_IPC")
        self.assertEqual(pairs["src-tauri/src/m32_sqlite_concurrency_tests.rs"],
                         "REVIEW_CI_ONLY")

    def test_08_live_checklist_and_operator_gates_are_not_promoted(self):
        self.assertIn("- [ ] **M32-007**", self.master)
        self.assertIn("AUCUNE case nouvelle clôturée", self.triage)
        self.assertIn("PRODUCT_FIRST_PARALLEL_SAFETY", self.triage)
        for token in ("IN_PROGRESS_NOT_ACCEPTED", "NOT_PROVEN",
                      "STOP_UNAVAILABLE", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                      "OPEN_NOT_REMEDIATED", "writer"):
            self.assertIn(token, self.triage)
        self.assertNotIn("AUTORISATION DE WRITE", self.triage)


class Pr215UnitDispositionContract(unittest.TestCase):
    """Offline guard of all 23 historical paths, no GitHub I/O or runtime admission."""
    @classmethod
    def setUpClass(cls):
        cls.text=(ROOT/"docs/qualification/M3_2_PR215_PER_PATH_DISPOSITION_20261121.md").read_text(encoding="utf-8")
        cls.lines=re.findall(
            r"^\| `([^`]+)` \| `([0-9a-f]{40})` \| `([0-9a-f]{40})` \| "
            r"`(IDENTICAL|DIFFERENT)` \| `([A-Z_]+)` \|",cls.text,re.M)

    @staticmethod
    def original_pr215_paths():
        text=REPORT.read_text(encoding="utf-8")
        one=text.split("### pr215 : identical (6)",1)[1].split("### pr215 : different (17)",1)[0]
        two=text.split("### pr215 : different (17)",1)[1].split("### pr215 : absent (0)",1)[0]
        return re.findall(r"^- `([^`]+)`$",one+two,re.M)

    def test_09_pr215_23_paths_unique_equal_historic_inventory(self):
        rows=self.lines
        paths=[r[0] for r in rows]
        self.assertEqual(len(rows),23)
        self.assertEqual(len(set(paths)),23)
        self.assertEqual(set(paths),set(self.original_pr215_paths()))
        self.assertEqual(sum(x[3]=="IDENTICAL" for x in rows),6)
        self.assertEqual(sum(x[3]=="DIFFERENT" for x in rows),17)
        for path,old,current,status,action in rows:
            self.assertEqual(old==current,status=="IDENTICAL",(path,status))
            self.assertNotIn(action,("ADMIT_WRITER","MERGE_DIRECT","RESTORE_OPERATOR"))

    def test_10_pr215_scope_no_runtime_or_historic_rewrite(self):
        rows=self.lines
        status={path:action for path,_,_,_,action in rows}
        self.assertEqual(sum(v=="KEEP_IDENTICAL_PROOF" for v in status.values()),6)
        self.assertEqual(sum(v=="KEEP_CURRENT_DOC_NO_REBASE" for v in status.values()),13)
        self.assertEqual(status["src-tauri/src/m32_sqlite_vfs_preopen_tests.rs"],
                         "REVIEW_CFG_TEST_ONLY")
        self.assertEqual(status["tools/m32_rust_sqlite_open_inventory.py"],
                         "REVIEW_READONLY_INVENTORY")
        self.assertEqual(status["tools/test_m32_handoff_contract.py"],
                         "REVIEW_HANDOFF_GUARDS")
        self.assertEqual(status["tools/test_m32_rust_sqlite_open_inventory.py"],
                         "REVIEW_INVENTORY_TESTS")
        for fn in D3B:
            self.assertIn("fn "+fn+"()",VFS.read_text(encoding="utf-8"))
        self.assertIn("#[cfg(all(test, windows))]\nmod m32_sqlite_vfs_preopen_tests;",
                      LIB.read_text(encoding="utf-8"))
        self.assertIn("- [ ] **M32-007**",CHECKLIST.read_text(encoding="utf-8"))
        self.assertIn("PENDING_EXTERNAL_ATTESTATION(21/3/2)",self.text)
        self.assertIn("M3.2 IN_PROGRESS_NOT_ACCEPTED",self.text)

    def test_11_pr215_forged_path_or_sha_refused(self):
        rows=self.lines
        def guarded(items):
            names=[x[0] for x in items]
            if len(items)!=23 or len(set(names))!=23 or set(names)!=set(
                    self.original_pr215_paths()):
                raise ValueError("STOP absent duplicate or invented path")
            for path,old,now,relation,action in items:
                if (old==now)!=(relation=="IDENTICAL"):
                    raise ValueError("STOP forged SHA relation")
                if action not in ("KEEP_IDENTICAL_PROOF","KEEP_CURRENT_DOC_NO_REBASE",
                                  "REVIEW_CFG_TEST_ONLY","REVIEW_READONLY_INVENTORY",
                                  "REVIEW_HANDOFF_GUARDS","REVIEW_INVENTORY_TESTS"):
                    raise ValueError("STOP forbidden admission")
        guarded(rows)
        with self.assertRaisesRegex(ValueError,"duplicate"):
            guarded(rows[:-1]+[rows[0]])
        forged=list(rows);path,o,n,s,a=forged[0];forged[0]=(path,n,n,s,a)
        with self.assertRaisesRegex(ValueError,"SHA relation"):
            guarded(forged)
        forged=list(rows);path,o,n,s,a=forged[0];forged[0]=(path,o,n,s,"ADMIT_WRITER")
        with self.assertRaisesRegex(ValueError,"forbidden admission"):
            guarded(forged)


class Pr35PaginationCursorNonEquivalence(unittest.TestCase):
    """Archive comparison only; never imports old PR #35 pagination runtime."""

    def test_12_old_cursor_contract_not_claimed_by_current_id_pages(self):
        report=(ROOT/"docs/qualification/M3_2_PR35_CURSOR_NON_EQUIVALENCE_20261121.md").read_text(encoding="utf-8")
        source=(ROOT/"src/M32FictionalEventManualWorkshop.tsx").read_text(encoding="utf-8")
        self.assertIn("M32-007 [ ]",report)
        self.assertIn("cursor stale-snapshot veto NOT_PORTED",report)
        self.assertIn("MAX_CURSOR_BYTES=4096",report)
        self.assertIn("MAX_PAGE_SIZE=64",report)
        self.assertIn("FICTIONAL_HISTORY_PAGE_SIZES = [5, 10, 20]",source)
        self.assertIn("if (!FICTIONAL_HISTORY_PAGE_SIZES.some",source)
        self.assertNotIn("cursor fingerprint authority proven",report)
        self.assertNotIn("ADMIT_WRITER",report)
        self.assertIn("- [ ] **M32-007**",CHECKLIST.read_text(encoding="utf-8"))

    def test_13_cannot_promote_old_cursor_as_writer_proof(self):
        report=(ROOT/"docs/qualification/M3_2_PR35_CURSOR_NON_EQUIVALENCE_20261121.md").read_text(encoding="utf-8")
        def guard(text):
            if "NOT_PORTED" not in text or "OPEN_NOT_ACCEPTED" not in text:
                raise ValueError("STOP old cursor promoted")
            if "same function" in text or "cursor fingerprint authority proven" in text:
                raise ValueError("STOP unsafe equivalence")
        guard(report)
        with self.assertRaisesRegex(ValueError,"promoted"):
            guard(report.replace("NOT_PORTED","REUSED_AS_IS"))
        with self.assertRaisesRegex(ValueError,"unsafe equivalence"):
            guard(report + "\nsame function\n")

class Pr35FullTreeScoping(unittest.TestCase):
    """Git blob triage only; no writer admission."""

    @classmethod
    def setUpClass(cls):
        cls.doc=(ROOT/"docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md").read_text(encoding="utf-8")
        cls.rows=[line.strip("| ").split(" | ") for line in cls.doc.splitlines()
                  if line.startswith("| `")]

    def test_14_unique_path_counts_and_sha_relations(self):
        self.assertEqual(len(self.rows),84)
        self.assertEqual(len({r[0] for r in self.rows}),84)
        self.assertEqual([sum(r[3]==s for r in self.rows) for s in ("IDENTICAL","DIVERGENT","ABSENT")],[5,11,68])
        for path,old,now,state,action in self.rows:
            self.assertEqual(len(old),42)
            if state=="IDENTICAL": self.assertEqual(old,now)
            elif state=="ABSENT": self.assertEqual(now,"ABSENT")
            else: self.assertNotEqual(old,now)
        for key in ("M32-007","M32-050"):
            self.assertIn(f"- [ ] **{key}**",CHECKLIST.read_text(encoding="utf-8"))

    def test_15_absent_groups_remain_non_admitted(self):
        absent=[r[0].strip(chr(96)) for r in self.rows if r[3]=="ABSENT"]
        self.assertEqual(sum(s.startswith("docs/") for s in absent),26)
        self.assertEqual(sum(s.startswith("tools/test_") for s in absent),20)
        self.assertEqual(sum(s.startswith("tools/") and not s.startswith("tools/test_") for s in absent),20)
        self.assertEqual(sum(s.startswith("src-tauri/") for s in absent),2)
        self.assertIn("M32-007 [ ] et M32-050 [ ] OPEN_NOT_ACCEPTED",self.doc)
        self.assertIn("DRAFT",self.doc)
        self.assertIn("NOT_PROVEN",self.doc)

class Pr215FourReviewCoverageSourceContract(unittest.TestCase):
    """Named tests and scoped old/modern review only; no admission of the writer."""

    @classmethod
    def setUpClass(cls):
        cls.doc=(ROOT/"docs/qualification/M3_2_PR215_FOUR_REVIEW_SOURCE_TEST_COVERAGE_20261121.md").read_text(encoding="utf-8")
        cls.rows=[line.strip("| ").split(" | ") for line in cls.doc.splitlines()
                  if line.startswith("| `")]

    def test_16_four_scoped_paths_keep_review_nonadmission(self):
        self.assertEqual(len(self.rows),4)
        self.assertEqual(len({r[0] for r in self.rows}),4)
        self.assertEqual([r[-1] for r in self.rows],[
            "REVIEW_CFG_TEST_ONLY","REVIEW_READONLY_INVENTORY",
            "REVIEW_HANDOFF_GUARDS","REVIEW_INVENTORY_TESTS"])
        self.assertIn("145 noms anciens sur 152",self.doc)
        self.assertIn("les 7 absents",self.doc)
        self.assertIn("26/26",self.doc)
        self.assertIn("41/41",self.doc)
        self.assertIn("- [ ] **M32-007**",CHECKLIST.read_text(encoding="utf-8"))
        self.assertIn("- [ ] **M32-050**",CHECKLIST.read_text(encoding="utf-8"))

    def test_17_renamed_tests_are_not_claimed_as_runtime_proof(self):
        self.assertIn("Noms disparus ≠ garanties perdues",self.doc)
        self.assertIn("OPEN_NOT_ACCEPTED",self.doc)
        self.assertIn("D3b-4/5",self.doc)
        self.assertIn("R3/R4",self.doc)
        self.assertIn("NOT_PROVEN",self.doc)

class Pr215SevenOldHandoffScopesContract(unittest.TestCase):
    """Old historical domains may be referenced, never auto-admitted."""

    def test_18_old_handoff_documents_exist_but_not_equivalence(self):
        path=ROOT/"docs/qualification/M3_2_PR215_SEVEN_OLD_HANDOFF_ASSERTION_SCOPES_20261121.md"
        report=path.read_text(encoding="utf-8")
        rows=[s for s in report.splitlines() if s.startswith("| 1") and
              "REVIEW_ASSERTIONS_NOT_PORTED" in s]
        self.assertEqual(len(rows),7)
        docs=[row.split(" | ")[2].strip("`") for row in rows]
        # Each of seven sources may cite the same historical design file.
        self.assertEqual(len(docs),7)
        self.assertTrue(all((ROOT/"docs/qualification"/d).is_file() for d in docs))
        self.assertIn("aucune exigence ne peut être fermée",report)
        self.assertIn("- [ ] **M32-007**",CHECKLIST.read_text(encoding="utf-8"))
        self.assertIn("OPEN_NOT_ACCEPTED",report)
        self.assertIn("NOT_PROVEN",report)

class Pr215Old146147AssertionReview(unittest.TestCase):
    def test_19_old_146_147_assertions_remain_unported(self):
        report=(ROOT/"docs/qualification/M3_2_PR215_OLD_HANDOFF_146_147_ASSERTION_REVIEW_20261121.md").read_text(encoding="utf-8")
        self.assertEqual(report.count("REVIEW_OLD_ASSERTIONS_NOT_PORTED"),2)
        for term in ("next_production_writer_custody_design_study_20261028",
                     "owner_p1_same_sid_ollama_design_decision_20261028",
                     "candidate_ci_qualified=false","external_writer_absence=NOT_PROVEN",
                     "a0_existing_profile_cross_process=STOP",
                     "Aucune équivalence","OPEN_NOT_ACCEPTED","R1–R9 NOT_PROVEN"):
            self.assertIn(term,report)
        check=CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("- [ ] **M32-007**",check)
        self.assertIn("- [ ] **M32-050**",check)

class Pr215Old148To152AssertionReview(unittest.TestCase):
    def test_20_five_historical_assertion_domains_are_not_reused_or_admitted(self):
        report=(ROOT/"docs/qualification/M3_2_PR215_OLD_HANDOFF_148_152_ASSERTION_REVIEW_20261121.md").read_text(encoding="utf-8")
        self.assertEqual(report.count("REVIEW_ASSERTIONS_NOT_PORTED"),5)
        for key in ("next_p1_single_owner_session_proof_plan_20261028",
                    "next_p1_d2_disposable_integrated_session_20261028",
                    "next_p1_d3_wal_shm_crash_restart_documentary_20261028",
                    "next_p1_d3a_wal_shm_disposable_windows_fixture_20261028",
                    "next_p1_d3b_disposable_crash_restart_refusal_fixture_20261028"):
            self.assertIn(key,report)
        for token in ("aucune recovery", "NOT_PROVEN","OPEN_NOT_ACCEPTED",
                      "R1–R9 NOT_PROVEN","Protect main",
                      "aucun code porté"):
            self.assertIn(token,report)
        checklist=CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("- [ ] **M32-007**",checklist)
        self.assertIn("- [ ] **M32-050**",checklist)

class Pr215FourReviewLiteralOnlyScope(unittest.TestCase):
    def test_21_four_paths_remain_review_non_accepted_after_literal_triage(self):
        report=(ROOT/"docs/qualification/M3_2_PR215_FOUR_REVIEW_LITERAL_SCOPE_AUDIT_20261121.md").read_text(encoding="utf-8")
        self.assertEqual(report.count("| REVIEW_NON_ACCEPTED |"),4)
        for name in ("m32_sqlite_vfs_preopen_tests.rs",
                     "m32_rust_sqlite_open_inventory.py",
                     "test_m32_rust_sqlite_open_inventory.py",
                     "test_m32_handoff_contract.py",
                     "M3_2_PR215_OLD_HANDOFF_146_147_ASSERTION_REVIEW_20261121.md",
                     "M3_2_PR215_OLD_HANDOFF_148_152_ASSERTION_REVIEW_20261121.md",
                     "aucune preuve", "OPEN_NOT_ACCEPTED", "R1–R9 NOT_PROVEN"):
            self.assertIn(name,report)
        check=CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("- [ ] **M32-007**",check)
        self.assertIn("- [ ] **M32-050**",check)


class Pr35AbsentRustSafetyEvidence(unittest.TestCase):
    """Scoped textual negatives, not a live SQLite, preflight or IPC proof."""

    CASES = (
        "two_connections_hide_uncommitted_chain_and_serialize_writers",
        "rollback_of_withdrawal_and_replacement_is_atomic_across_connections",
        "two_connection_readonly_and_cycle_guards_reject_cross_handle_bypass",
    )
    API = (
        "create_anchor", "create_precedence", "decide_precedence",
        "restate_revoked_precedence", "revoke_restatement",
        "succeed_withdrawn_restatement", "revoke_successor",
        "list_active_precedence_graph", "append_chain_correction",
        "revoke_chain_correction", "create_calendar",
    )

    @classmethod
    def setUpClass(cls):
        cls.lib = LIB.read_text(encoding="utf-8")
        cls.chron = (ROOT / "src-tauri/src/m32_manual_chronology.rs").read_text(encoding="utf-8")
        cls.doc = (ROOT / "docs/qualification/"
                   "M3_2_PR35_TWO_ABSENT_RUST_MODULES_SCOPE_20261122.md").read_text(encoding="utf-8")
        cls.checklist = CHECKLIST.read_text(encoding="utf-8")

    @classmethod
    def guard(cls, lib, chron, doc, checklist):
        if "#[cfg(test)]\nmod m32_manual_chronology;" not in lib:
            raise ValueError("STOP chronology test-only scope lost")
        for name in ("m32_isolated_preflight", "m32_sqlite_concurrency_tests"):
            if re.search(r"\bmod\s+" + name + r"\s*;", lib):
                raise ValueError("STOP historical module registration " + name)
        if "m32_isolated_preflight_status" in lib:
            raise ValueError("STOP historical command registration")
        for name in cls.API:
            if not re.search(r"\bfn\s+" + name + r"\s*\(", chron):
                raise ValueError("STOP modern chronology symbol drift " + name)
            if name not in doc:
                raise ValueError("STOP missing API scope " + name)
        for name in cls.CASES:
            if name not in doc:
                raise ValueError("STOP historical SQLite test unreviewed " + name)
        for marker in ("BLOCK_RUNTIME_IPC", "REVIEW_CI_ONLY", "NOT_PORTED",
                       "NOT_PROVEN", "OPEN_NOT_ACCEPTED", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                       "source-only"):
            if marker not in doc:
                raise ValueError("STOP false old Rust admission " + marker)
        for task in ("M32-007", "M32-050"):
            if "- [ ] **" + task + "**" not in checklist:
                raise ValueError("STOP legacy reconciliation prematurely closed " + task)
        return len(cls.CASES), len(cls.API)

    def test_22_three_old_sqlite_cases_and_eleven_modern_symbols_not_admitted(self):
        self.assertEqual(self.guard(self.lib, self.chron, self.doc, self.checklist), (3, 11))

    def test_23_old_runtime_preflight_and_concurrency_mod_registration_refused(self):
        for candidate in (
            "\nmod m32_isolated_preflight;",
            "\n#[cfg(test)]\nmod m32_sqlite_concurrency_tests;",
            "\n#[cfg(all(test, windows))]\nmod m32_isolated_preflight;",
            "\nuse crate::m32_isolated_preflight_status;",
        ):
            with self.subTest(candidate=candidate), self.assertRaisesRegex(
                ValueError, "historical module registration|historical command registration"
            ):
                self.guard(self.lib + candidate, self.chron, self.doc, self.checklist)

    def test_24_old_code_or_safety_scope_falsification_refused(self):
        with self.assertRaisesRegex(ValueError, "chronology test-only"):
            self.guard(self.lib.replace("#[cfg(test)]\nmod m32_manual_chronology;",
                                        "mod m32_manual_chronology;"),
                       self.chron, self.doc, self.checklist)
        with self.assertRaisesRegex(ValueError, "modern chronology symbol drift"):
            self.guard(self.lib, re.sub(r"\bfn\s+append_chain_correction\s*\(",
                                        "fn renamed_chain_correction(",
                                        self.chron, count=1), self.doc, self.checklist)
        with self.assertRaisesRegex(ValueError, "old Rust admission"):
            self.guard(self.lib, self.chron, self.doc.replace("NOT_PORTED", "ADMITTED"),
                       self.checklist)
        with self.assertRaisesRegex(ValueError, "prematurely closed"):
            self.guard(self.lib, self.chron, self.doc,
                       self.checklist.replace("- [ ] **M32-007**", "- [x] **M32-007**"))


class Pr35TwentyHistoricalPythonPairsSourceOnly(unittest.TestCase):
    """Historic absent 20 scripts + 20 tests: names only, never import their code."""

    AUDIT = ROOT / "docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md"
    REPORT = ROOT / "docs/qualification/M3_2_PR35_TWENTY_PYTHON_PAIRS_SCOPE_20261122.md"

    @staticmethod
    def guard(audit: str, report: str, checklist: str):
        absent = re.findall(
            r"(?m)^\| \`([^\`]+)\` \| \`[0-9a-f]{40}\` \| ABSENT \| ABSENT \|",
            audit,
        )
        scripts = sorted(x for x in absent if x.startswith("tools/m3_2_"))
        tests = sorted(x for x in absent if x.startswith("tools/test_m3_2_"))
        if (len(scripts), len(tests), len(set(absent))) != (20, 20, 68):
            raise ValueError("STOP PR35 20+20+68 source inventory drift")
        expected = [(s, "tools/test_" + s.removeprefix("tools/")) for s in scripts]
        if sorted(tests) != sorted(t for _, t in expected):
            raise ValueError("STOP PR35 paired test inventory drift")
        observed = re.findall(
            r"(?m)^\| \`(tools/m3_2_[^\`]+\.py)\` \| "
            r"\`(tools/test_m3_2_[^\`]+\.py)\` \| (NOT_PORTED_SOURCE_ONLY) \|$",
            report,
        )
        if sorted(observed) != sorted((s, t, "NOT_PORTED_SOURCE_ONLY") for s, t in expected):
            raise ValueError("STOP PR35 pair decision/evidence mismatch")
        for s, t in expected:
            if (ROOT / s).exists() or (ROOT / t).exists():
                raise ValueError("STOP historic Python source imported without fresh review")
        for marker in (
            "NO_SEMANTIC_EQUIVALENCE", "NO_RUNTIME_ADMISSION",
            "NOT_PROVEN", "PRODUCT_FIRST_PARALLEL_SAFETY",
            "G3 STOP_UNAVAILABLE", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
            "M32-007 [ ]", "M32-050 [ ]",
        ):
            if marker not in report:
                raise ValueError("STOP PR35 Python boundary lost " + marker)
        for task in ("M32-007", "M32-050"):
            if f"- [ ] **{task}**" not in checklist:
                raise ValueError("STOP PR35 false checklist closure " + task)
        return len(expected), len(absent)

    def test_25_twenty_python_modules_pair_with_twenty_historic_tests(self):
        self.assertEqual(self.guard(self.AUDIT.read_text(encoding="utf-8"),
                                    self.REPORT.read_text(encoding="utf-8"),
                                    CHECKLIST.read_text(encoding="utf-8")), (20, 68))

    def test_26_lost_or_forged_historic_pairs_are_refused(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        check = CHECKLIST.read_text(encoding="utf-8")
        first = next(line for line in report.splitlines() if line.startswith("| `tools/m3_2_"))
        with self.assertRaisesRegex(ValueError, "pair decision/evidence mismatch"):
            self.guard(audit, report.replace(first, ""), check)
        with self.assertRaisesRegex(ValueError, "pair decision/evidence mismatch"):
            self.guard(audit, report.replace(first, first.replace(
                "NOT_PORTED_SOURCE_ONLY", "ADMITTED")), check)
        with self.assertRaisesRegex(ValueError, "source inventory drift"):
            self.guard(audit.replace("| ABSENT | ABSENT |", "| INVENTED | ABSENT |", 1),
                       report, check)

    def test_27_no_false_python_admission_or_checklist_promotion(self):
        audit = self.AUDIT.read_text(encoding="utf-8")
        report = self.REPORT.read_text(encoding="utf-8")
        check = CHECKLIST.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Python boundary lost"):
            self.guard(audit, report.replace("NO_RUNTIME_ADMISSION", "RUNTIME_ADMITTED"), check)
        with self.assertRaisesRegex(ValueError, "false checklist closure"):
            self.guard(audit, report,
                       check.replace("- [ ] **M32-050**", "- [x] **M32-050**"))


class Pr35Stage24To29PairedHistoricalTestReview(unittest.TestCase):
    """Recorded Git blob identities and 110 method names are NOT test PASS."""

    REPORT = ROOT / "docs/qualification/M3_2_PR35_STAGE24_25_29_SCOPED_SOURCE_REVIEW_20261122.md"
    AUDIT = ROOT / "docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md"
    PAIRS = (
        (24, "navigation", "5826f9c79532e11520e139637859b1d778f92e7f",
         "91fabd546a22fb8f98481f7f0b8cba85600a1490", 50),
        (25, "comparison", "9f6dfd8d09cb4829b6b2ee168f0a1043212d1885",
         "6488ec2fdec95566358e48d0c6ef1ddbb5d7fad7", 26),
        (29, "selection_review", "a6985f28f1f91cd4afc415469ef59c11f867c5c4",
         "86dac0ab3aa3ae3fe524c2d77a406fd1852d2160", 34),
    )

    @classmethod
    def guard(cls, report, audit, checklist):
        for stage, stem, source_sha, test_sha, expected_count in cls.PAIRS:
            source = f"tools/m3_2_chronology_{stem}_reference.py"
            test = f"tools/test_m3_2_chronology_{stem}_reference.py"
            row = (f"| {stage} | `{source}` | `{test}` | `{source_sha}` | "
                   f"`{test_sha}` | {expected_count} | SOURCE_REVIEW_ONLY_NOT_EXECUTED |")
            if row not in report:
                raise ValueError("STOP historic test signature provenance drift " + stem)
            for filename, sha in ((source, source_sha), (test, test_sha)):
                if f"| `{filename}` | `{sha}` | ABSENT | ABSENT |" not in audit:
                    raise ValueError("STOP historic blob reference drift " + filename)
                if (ROOT / filename).exists():
                    raise ValueError("STOP old source reintroduced " + filename)
        if report.count("REVIEW_ONLY_NOT_PORTED") != 3:
            raise ValueError("STOP historic module review status drift")
        for token in ("TOTAL_110_METHOD_NAMES_SOURCE_INSPECTED_NOT_EXECUTED",
                      "NO_SEMANTIC_EQUIVALENCE", "NO_AUTO_PORT", "NO_RUNTIME_ADMISSION",
                      "OPEN_NOT_ACCEPTED", "R1–R9 NOT_PROVEN",
                      "M32-007 [ ]", "M32-050 [ ]", "5 des 20", "15 restent"):
            if token not in report:
                raise ValueError("STOP false historic test admission " + token)
        for task in ("M32-007", "M32-050"):
            if f"- [ ] **{task}**" not in checklist:
                raise ValueError("STOP false historic test checklist closure " + task)
        return len(cls.PAIRS), sum(p[4] for p in cls.PAIRS)

    def test_28_three_paired_stage24_25_29_sha_and_counts_are_source_only(self):
        self.assertEqual(self.guard(self.REPORT.read_text(encoding="utf-8"),
                                    self.AUDIT.read_text(encoding="utf-8"),
                                    CHECKLIST.read_text(encoding="utf-8")), (3, 110))

    def test_29_forged_blob_count_or_admission_is_refused(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        for bad in (report.replace(" | 50 | SOURCE_REVIEW_ONLY_NOT_EXECUTED |",
                                   " | 51 | SOURCE_REVIEW_ONLY_NOT_EXECUTED |"),
                    report.replace("91fabd546a22fb8f98481f7f0b8cba85600a1490",
                                   "0"*40),
                    report.replace("NO_SEMANTIC_EQUIVALENCE", "SEMANTIC_EQUIVALENCE")):
            with self.subTest(candidate=bad[:30]), self.assertRaisesRegex(
                    ValueError, "provenance drift|false historic test admission"):
                self.guard(bad, audit, checklist)

    def test_30_false_requirement_closure_is_refused(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "false historic test checklist closure"):
            self.guard(report, audit,
                       checklist.replace("- [ ] **M32-050**", "- [x] **M32-050**"))


class Pr35RemainingFifteenPythonPairsSourceOnly(unittest.TestCase):
    """Historic 15 Python pairs: SHA+method-name source inventory, no execution."""

    DOCS = (
        ROOT / "docs/qualification/M3_2_PR35_STAGE11_18_AUTHORITY_SOURCES_READONLY_SCOPE_20261122.md",
        ROOT / "docs/qualification/M3_2_PR35_STAGE19_20_22_SOURCE_SCOPE_20261122.md",
        ROOT / "docs/qualification/M3_2_PR35_STAGE26_27_28_WITNESS_SOURCE_AUDIT_20261122.md",
        ROOT / "docs/qualification/M3_2_PR35_STAGE30_31_32_BATCH_HANDOFF_SOURCE_REVIEW_20261122.md",
    )
    PAIRS = (
        ("tools/m3_2_operator_readonly_gate.py", "tools/test_m3_2_operator_readonly_gate.py", "6a2281e9b12e2a83f282e1bfd936eb3314ef6108", "ca7ada469eec00f07d984be8aefc4f881661c0c7", 8, 0),
        ("tools/m3_2_multiroot_readonly.py", "tools/test_m3_2_multiroot_readonly.py", "171fdd7c067f217c2985d510908326507a187d6b", "87d1fe01a8f193a2efddc82f53a1e2d230b4b1ef", 12, 0),
        ("tools/m3_2_independent_authority_gate.py", "tools/test_m3_2_independent_authority_gate.py", "baafb72e571de8dc85986749a7c9755ef7f5ca44", "d03b32d9e6d18be114fd7096392c6e73f0301088", 14, 0),
        ("tools/m3_2_m31_semantic_readonly.py", "tools/test_m3_2_m31_semantic_readonly.py", "82044b24c8f70fd9c5f414c53cd20039e98ae682", "d1831b3c2b3b3f09f0f87cd99608fc18123464a4", 21, 0),
        ("tools/m3_2_direct_custody_readonly.py", "tools/test_m3_2_direct_custody_readonly.py", "b50f86359708e0ccc37679d77a50c79192d58de8", "fd98291dd4590d9c446415bcc0c1d177dd2bafa8", 24, 0),
        ("tools/m3_2_isolated_v7_physical_readonly.py", "tools/test_m3_2_isolated_v7_physical_readonly.py", "2a6bb6f67eb7e2c97483b25d2e27f5e3dbe37acd", "0b1cd5393ff6943126b4ee8e0fb4bc655ef4fec5", 18, 0),
        ("tools/m3_2_provenance_triage.py", "tools/test_m3_2_provenance_triage.py", "0f40cc90905b2e22dcde364b3896a86dc7b62200", "6703160f7ca532f6c9c8f99ece2a84e5b01187da", 33, 1),
        ("tools/m3_2_supersession_reference.py", "tools/test_m3_2_supersession_reference.py", "77ff7cf61e8fe6df581cab3ba83b21cd4e0c5c3a", "cc91ab96c0928974a4f01230a4365dde9e88862b", 25, 1),
        ("tools/m3_2_chronology_presentation_reference.py", "tools/test_m3_2_chronology_presentation_reference.py", "811f29ba968a401fbafa3dbf423ddee0527c505b", "44f30a03c4fe751513394e1a5f1ab0a1646590cc", 25, 1),
        ("tools/m3_2_chronology_witness_reference.py", "tools/test_m3_2_chronology_witness_reference.py", "8dfdf8b706593c84be5b151b61080ae44c3dd007", "11e93ed4e45f5da5f488bb01b21e8eb6e05b49f0", 32, 2),
        ("tools/m3_2_chronology_witness_presentation_reference.py", "tools/test_m3_2_chronology_witness_presentation_reference.py", "c346fbf923ca4e6bf87d188c846b167ea4c479af", "a7b64a754ee42b74c4e8bb0d65e83cb929cd0d8c", 30, 2),
        ("tools/m3_2_chronology_witness_consultation_reference.py", "tools/test_m3_2_chronology_witness_consultation_reference.py", "93969516981211ffd3723daaa222121c55cf9773", "9b4c19e7c3a62d6f56566655ac489af26e31cc4e", 30, 2),
        ("tools/m3_2_chronology_comparison_batch_reference.py", "tools/test_m3_2_chronology_comparison_batch_reference.py", "fabc802887e5f7960c0fac255021050d87e03339", "f9696030d20321d9dc9789a1fb12ce5cca3b39c3", 41, 3),
        ("tools/m3_2_chronology_batch_coherence_reference.py", "tools/test_m3_2_chronology_batch_coherence_reference.py", "092906f5d7c1f71303f3eff0659eebaa42926c9f", "cfea445305060c139f62248f8b01cb812a169296", 37, 3),
        ("tools/m3_2_chronology_readonly_handoff_reference.py", "tools/test_m3_2_chronology_readonly_handoff_reference.py", "0f3607ad9e74dd1934e0e0ab21a39dd25e9587f2", "131887a4552551eda574f55ad64538026478abe0", 34, 3),
    )
    AUDIT = ROOT / "docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md"

    @classmethod
    def guard(cls, reports, audit, checklist):
        if len(reports) != 4:
            raise ValueError("STOP historic report inventory drift")
        for report in reports:
            for token in ("NO_SEMANTIC_EQUIVALENCE", "NO_AUTO_PORT",
                          "NO_RUNTIME_ADMISSION", "OPEN_NOT_ACCEPTED",
                          "R1–R9 NOT_PROVEN", "M32-007 [ ]", "M32-050 [ ]"):
                if token not in report:
                    raise ValueError("STOP historic source false authority " + token)
        for source, test, sha, test_sha, count, report_id in cls.PAIRS:
            # Stage26/27/28 report uses short names; others use full paths.
            a = source.removeprefix("tools/") if report_id == 2 else source
            b = test.removeprefix("tools/") if report_id == 2 else test
            lines = [line for line in reports[report_id].splitlines()
                     if line.startswith("|") and f"`{a}`" in line
                     and f"`{b}`" in line and f"`{sha}`" in line
                     and f"`{test_sha}`" in line and f"**{count}**" in line]
            if len(lines) != 1:
                raise ValueError("STOP historic paired blob/count provenance drift " + source)
            for name, blob in ((source, sha), (test, test_sha)):
                if f"| `{name}` | `{blob}` | ABSENT | ABSENT |" not in audit:
                    raise ValueError("STOP historic Git blob audit mismatch " + name)
                if (ROOT / name).exists():
                    raise ValueError("STOP old Python module imported " + name)
        for req in ("M32-007", "M32-050"):
            if f"- [ ] **{req}**" not in checklist:
                raise ValueError("STOP false historical checklist closure " + req)
        if ("20/20 SOURCE_DESCRIBED_NOT_EQUIVALENT" not in reports[0] or
                "0/20 PORTED" not in reports[0] or
                "0/20 ADMITTED" not in reports[0]):
            raise ValueError("STOP false historical equivalence or admission")
        return len(cls.PAIRS), sum(row[4] for row in cls.PAIRS)

    def test_31_all_15_historic_pairs_have_immutable_blob_and_name_counts(self):
        reports = [path.read_text(encoding="utf-8") for path in self.DOCS]
        self.assertEqual(self.guard(reports, self.AUDIT.read_text(encoding="utf-8"),
                                    CHECKLIST.read_text(encoding="utf-8")), (15, 384))

    def test_32_spoofed_historic_sha_or_method_count_fails_closed(self):
        reports = [p.read_text(encoding="utf-8") for p in self.DOCS]
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        for changed in (reports[0].replace("6a2281e9b12e2a83f282e1bfd936eb3314ef6108",
                                           "0"*40),
                        reports[0].replace("**8**", "**9**", 1)):
            candidate = reports.copy()
            candidate[0] = changed
            with self.assertRaisesRegex(ValueError, "blob/count provenance drift"):
                self.guard(candidate, audit, checklist)

    def test_33_refuses_false_admission_and_legacy_checklist_closure(self):
        reports = [p.read_text(encoding="utf-8") for p in self.DOCS]
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        mutated = reports.copy()
        mutated[0] = mutated[0].replace("NO_RUNTIME_ADMISSION", "RUNTIME_ADMITTED")
        with self.assertRaisesRegex(ValueError, "false authority"):
            self.guard(mutated, audit, checklist)
        with self.assertRaisesRegex(ValueError, "false historical checklist closure"):
            self.guard(reports, audit,
                       checklist.replace("- [ ] **M32-007**", "- [x] **M32-007**"))


class Pr35TwentySixDocumentMetadata(unittest.TestCase):
    """26 immutable historic document blobs, no import or real operator access."""
    REPORT = ROOT / "docs/qualification/M3_2_PR35_26_ABSENT_DOCUMENTS_SOURCE_TRIAGE_20261123.md"
    AUDIT = ROOT / "docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md"
    DOCS = (
        ("docs/qualification/M3_2_ACTIVATION_MARKER_INVENTORY.md", "b5529fc9bdcec01478600e699ef0b547e7f8d560", "AUTHORITY"),
        ("docs/qualification/M3_2_DIRECT_READONLY_CUSTODY.md", "a82b76e5e55c57d3462ebfc081c0ece786a94b79", "AUTHORITY"),
        ("docs/qualification/M3_2_EXTERNAL_ATTESTATION_RESOLUTION_MATRIX.md", "673fd153df11b479f7bb4893fc8b54c7826f1464", "AUTHORITY"),
        ("docs/qualification/M3_2_INDEPENDENT_AUTHORITY_GATE.md", "0d5793f2250a2a9b8f2e23ed3c6a50b15177c99c", "AUTHORITY"),
        ("docs/qualification/M3_2_ISOLATED_IPC_PREFLIGHT.md", "2b2bd2bbc9f20687f7a0a65242f4cdec1aff2457", "AUTHORITY"),
        ("docs/qualification/M3_2_ISOLATED_V7_PHYSICAL_READONLY.md", "1211d66dd69e2d1bb703c434434e50d02703dbe5", "AUTHORITY"),
        ("docs/qualification/M3_2_M31_SEMANTIC_HARDENING.md", "31f01f45dcdfe4dc72c90ee36ea854dbe2c96f4c", "AUTHORITY"),
        ("docs/qualification/M3_2_M31_SEMANTIC_READONLY_GATE.md", "ee96c6a4abb91985aaa7069747ea1a7fc7e4d240", "AUTHORITY"),
        ("docs/qualification/M3_2_MULTIROOT_READONLY_GATE.md", "a1a515312d40f415ca014888246d820c6ec40aa5", "AUTHORITY"),
        ("docs/qualification/M3_2_POST_RESTART_GATE.md", "0be718bc9e004daf0abba6e6591cc65e958d00c4", "AUTHORITY"),
        ("docs/qualification/M3_2_PROVENANCE_CLAIM_TRIAGE.md", "9380c98f9bbbd2147e1db0c2fbe9d6c72c425337", "AUTHORITY"),
        ("docs/qualification/M3_2_APPEND_ONLY_SUPERSESSION_DESIGN.md", "28a93cb252bdef2b8aba68d3ec369dceccdd83b2", "DESIGN"),
        ("docs/qualification/M3_2_MANUAL_CHRONOLOGY_STAGE1.md", "2d35b688093bfd75032dfae7082a3ea353857d7f", "DESIGN"),
        ("docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md", "7372b2c332821faab238dfc4ed113aff963feece", "DESIGN"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_BATCH_COHERENCE.md", "4238b941a6157a924082813d0c2549aee1bd8b36", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON.md", "619cc24ea5ad6f899745b30524b9996242faa6cd", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_COMPARISON_BATCH.md", "9eb25d602bc9751bfd57a090a638aaffb4f2f367", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_NAVIGATION.md", "02115fe271c6849cdffa60dd8db039927a10e62b", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_PAGINATION.md", "9786816bb428abfc703b939f8c2b33bdbc7266f2", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_PRESENTATION.md", "809e1772e4b212565f11af1ecec7d9bfdb989cac", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_PROJECTION.md", "0650d66851135030a961e506eb1c8cc9c5ebb737", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_SELECTION_REVIEW.md", "fe8849a7a4a30d6718d69294f1f34b167db422d8", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS.md", "62740aed0cc1d959cd1a3abc0ef111f827c3f95e", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_CONSULTATION.md", "6ad6585df74e64f59077a8941ad74eb266d7266a", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_CHRONOLOGY_WITNESS_PRESENTATION.md", "d92c6d9f03b92a77613023bed8ff58c2296ecfa1", "SYNTHETIC"),
        ("docs/qualification/M3_2_READONLY_HANDOFF_REFERENCE.md", "a0215b0a5b47fabe3d1b7f2871b71f3a4fb02b7c", "SYNTHETIC"),
    )

    @classmethod
    def guard(cls, report, audit, checklist):
        if len(cls.DOCS) != 26 or len({x[0] for x in cls.DOCS}) != 26:
            raise ValueError("STOP document inventory")
        for token in ("SOURCE_ONLY_CANDIDATE_UNQUALIFIED", "NO_SEMANTIC_EQUIVALENCE",
                      "NO_AUTO_PORT", "NO_RUNTIME_ADMISSION", "OPEN_NOT_ACCEPTED",
                      "26/26 SOURCE_DESCRIBED_NOT_ADMITTED", "R1–R9 NOT_PROVEN"):
            if token not in report:
                raise ValueError("STOP false historic document authority " + token)
        groups = {"AUTHORITY": 0, "DESIGN": 0, "SYNTHETIC": 0}
        for path, blob, category in cls.DOCS:
            if category not in groups or (ROOT / path).exists():
                raise ValueError("STOP historical document import " + path)
            groups[category] += 1
            if report.count(f"| `{path}` | `{blob}` | {category} | HISTORICAL_SOURCE_ONLY |") != 1:
                raise ValueError("STOP historic document SHA mismatch " + path)
            if f"| `{path}` | `{blob}` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |" not in audit:
                raise ValueError("STOP historic document audit mismatch " + path)
        if groups != {"AUTHORITY": 11, "DESIGN": 3, "SYNTHETIC": 12}:
            raise ValueError("STOP historical classification drift")
        for task in ("M32-007", "M32-050", "M32-078"):
            if f"- [ ] **{task}**" not in checklist:
                raise ValueError("STOP false historic document checklist closure " + task)
        return len(cls.DOCS)

    def test_34_all_historic_documents_source_only(self):
        self.assertEqual(self.guard(self.REPORT.read_text(encoding="utf-8"),
                                    self.AUDIT.read_text(encoding="utf-8"),
                                    CHECKLIST.read_text(encoding="utf-8")), 26)

    def test_35_refuses_forged_blob_and_false_authority(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            self.guard(report.replace("b5529fc9bdcec01478600e699ef0b547e7f8d560", "0"*40), audit, checklist)
        with self.assertRaisesRegex(ValueError, "false historic document authority"):
            self.guard(report.replace("NO_RUNTIME_ADMISSION", "RUNTIME_ADMISSION"), audit, checklist)

    def test_36_refuses_false_legacy_requirement_closure(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        for task in ("M32-007", "M32-050", "M32-078"):
            with self.subTest(task=task), self.assertRaisesRegex(ValueError, "false historic document checklist closure"):
                self.guard(report, audit, checklist.replace(f"- [ ] **{task}**", f"- [x] **{task}**"))


class Pr35ElevenDivergentSourceOnly(unittest.TestCase):
    """Exact historical/current Git blob pairs; never restore legacy code."""
    REPORT = ROOT / "docs/qualification/M3_2_PR35_ELEVEN_DIVERGENT_BLOBS_SOURCE_REVIEW_20261123.md"
    AUDIT = ROOT / "docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md"
    ROWS = (
        (".github/workflows/m0-ci.yml", "e12bf78e22ba6eb71ed7678a0ddf4ad54fa35e27", "c35a8f076b2770e676f63da48e9a93b6cc495b81", "BUILD_SECURITY"),
        ("README.md", "e0191b8f01d84fc97db40f1d5eb5031f0364d06d", "9e3408aeb459170a006a60e94721fabcb1595f3b", "CONTINUITY"),
        ("docs/continuity/NEXT.md", "b24b245b02c423f26f1a2315de0a6110a724eca0", "6aa0cf07e526aef18977a0d5c42546eaf17f6e80", "CONTINUITY"),
        ("docs/continuity/STATE.md", "0d05054b5bb5d7e7bbcffab846d09285f3272067", "635f6c15eee06e7502a71a37cd80e35c135592e6", "CONTINUITY"),
        ("src-tauri/Cargo.toml", "9c0c286062dbf3c881b7d76d1a1ea45d85385766", "50a36053f4772bd11769d2cd13a5b8b633038a78", "BUILD_SECURITY"),
        ("src-tauri/build.rs", "32adde45c871d1c31639d1debc0fe779c0c69881", "d860e1e6a7cac333c3cc0bc9cb67faf286b07d69", "BUILD_SECURITY"),
        ("src-tauri/sql/m3_2_chronology_decisions_candidate.sql", "fbd2a6244e6356a68e4fa707a7395fcbafe0449e", "786dc766769467ab6bf3243971855da31ff0dfbd", "SQL_FIXTURE"),
        ("src-tauri/src/lib.rs", "22cd1cdcbc5ecd9ae08bfa5e926ea56834c6a343", "25796459e334f040f7e8ec8e677636f37f6dc947", "BUILD_SECURITY"),
        ("src-tauri/src/m32_manual_chronology.rs", "f75e4bc7787b60ac345cbe137355f4888243829c", "c5542fed19b338752563f144a9484a34f9f79688", "ISOLATED_PRODUCT"),
        ("src/M32ChronologyPreview.tsx", "d7b6e5972a4730f487d346ae4e8116a9f7d84bca", "f57a48f26b4460d9f0aefec23b1880e722a3d860", "ISOLATED_PRODUCT"),
        ("src/m32ChronologyPreview.test.tsx", "bdc8e0b5ec3d22a784a864e81c82895915d2bc08", "c6aa039d3e8ad0db556dc1a7f53417d82f4c3193", "ISOLATED_PRODUCT"),
    )

    @classmethod
    def guard(cls, report, audit, checklist):
        if len(cls.ROWS) != 11 or len({row[0] for row in cls.ROWS}) != 11:
            raise ValueError("STOP divergent path partition")
        for marker in ("SOURCE_ONLY_CANDIDATE_UNQUALIFIED", "NO_RUNTIME_ADMISSION",
                       "NO_SEMANTIC_EQUIVALENCE", "NO_AUTO_PORT", "OPEN_NOT_ACCEPTED",
                       "11/11 SOURCE_SCOPED_NOT_ADMITTED", "0/11 PORTED", "0/11 ADMITTED",
                       "R1–R9 NOT_PROVEN"):
            if marker not in report:
                raise ValueError("STOP false legacy divergent authority " + marker)
        counts = {"BUILD_SECURITY": 0, "CONTINUITY": 0,
                  "ISOLATED_PRODUCT": 0, "SQL_FIXTURE": 0}
        for path, oldsha, mainsha, role in cls.ROWS:
            if role not in counts or oldsha == mainsha or not (ROOT / path).is_file():
                raise ValueError("STOP old divergent source restored or missing " + path)
            counts[role] += 1
            row = f"| `{path}` | `{oldsha}` | `{mainsha}` | {role} | REVIEW_CURRENT_DIFF_NO_OVERRIDE |"
            if report.count(row) != 1:
                raise ValueError("STOP divergent SHA or role drift " + path)
            matched = [line for line in audit.splitlines()
                       if line.startswith(f"| `{path}` | `{oldsha}` |")
                       and "| DIVERGENT | REVIEW_CURRENT_DIFF_NO_OVERRIDE |" in line]
            if len(matched) != 1:
                raise ValueError("STOP PR35 old audit mismatch " + path)
        if counts != {"BUILD_SECURITY": 4, "CONTINUITY": 3,
                      "ISOLATED_PRODUCT": 3, "SQL_FIXTURE": 1}:
            raise ValueError("STOP divergent scope partition")
        for task in ("M32-007", "M32-050", "M32-078"):
            if f"- [ ] **{task}**" not in checklist:
                raise ValueError("STOP false divergent requirement closure " + task)
        return 11

    def test_37_all_11_source_only_blob_pairs_remain_divergent(self):
        self.assertEqual(self.guard(self.REPORT.read_text(encoding="utf-8"),
                                    self.AUDIT.read_text(encoding="utf-8"),
                                    CHECKLIST.read_text(encoding="utf-8")), 11)

    def test_38_forged_blob_scope_and_false_admission_refused(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA or role drift"):
            self.guard(report.replace("e12bf78e22ba6eb71ed7678a0ddf4ad54fa35e27",
                                      "0"*40), audit, checklist)
        with self.assertRaisesRegex(ValueError, "false legacy divergent authority"):
            self.guard(report.replace("NO_RUNTIME_ADMISSION", "RUNTIME_ADMITTED"), audit, checklist)

    def test_39_false_legacy_checklist_closure_refused(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        for task in ("M32-007", "M32-050", "M32-078"):
            with self.subTest(task=task), self.assertRaisesRegex(
                    ValueError, "false divergent requirement closure"):
                self.guard(report, audit, checklist.replace(
                    f"- [ ] **{task}**", f"- [x] **{task}**"))


class Pr35TwoAbsentRustSourceOnly(unittest.TestCase):
    """Historic two Rust paths are source-only; never revive old IPC or WAL tests."""
    REPORT = ROOT / "docs/qualification/M3_2_PR35_TWO_ABSENT_RUST_FILES_SOURCE_REVIEW_20261123.md"
    AUDIT = ROOT / "docs/qualification/M3_2_PR35_84_PATH_TREE_AUDIT_20261121.md"
    PATHS = (
        ("src-tauri/src/m32_isolated_preflight.rs", "49a41a233e342a0ea541f74c4cea7dfedcb887c5", "OLD_METADATA_ONLY_IPC", 3),
        ("src-tauri/src/m32_sqlite_concurrency_tests.rs", "a940fb0996ae9361c69768979969f4b29ad7f6aa", "CI_SCRATCH_SQLITE_TESTS", 3),
    )

    @classmethod
    def guard(cls, report, audit, checklist):
        if len(cls.PATHS) != 2:
            raise ValueError("STOP Rust scope")
        for marker in ("SOURCE_ONLY_CANDIDATE_UNQUALIFIED", "NO_AUTO_PORT",
                       "NO_RUNTIME_ADMISSION", "NO_SEMANTIC_EQUIVALENCE",
                       "2/2 ABSENT_NOT_ADMITTED", "0/2 PORTED", "0/2 ADMITTED",
                       "BLOCK_RUNTIME_IPC", "BLOCK_OPERATOR_SQLITE", "R1–R9 NOT_PROVEN"):
            if marker not in report:
                raise ValueError("STOP false Rust historical authority " + marker)
        for path, blob, role, count in cls.PATHS:
            if (ROOT / path).exists():
                raise ValueError("STOP historical Rust module restored " + path)
            if report.count(f"| `{path}` | `{blob}` | {role} | {count} | HISTORICAL_SOURCE_ONLY |") != 1:
                raise ValueError("STOP historical Rust SHA/count drift " + path)
            if f"| `{path}` | `{blob}` | ABSENT | ABSENT | REVIEW_ABSENT_NO_AUTO_PORT |" not in audit:
                raise ValueError("STOP Rust audit mismatch " + path)
        for task in ("M32-007", "M32-050", "M32-078"):
            if f"- [ ] **{task}**" not in checklist:
                raise ValueError("STOP false Rust checklist closure " + task)
        return len(cls.PATHS)

    def test_40_rust_two_legacy_source_hashes_and_current_absence(self):
        self.assertEqual(self.guard(self.REPORT.read_text(encoding="utf-8"),
                                    self.AUDIT.read_text(encoding="utf-8"),
                                    CHECKLIST.read_text(encoding="utf-8")), 2)

    def test_41_forged_old_rust_sha_or_runtime_admission_refused(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA/count drift"):
            self.guard(report.replace("49a41a233e342a0ea541f74c4cea7dfedcb887c5", "0"*40),
                       audit, checklist)
        with self.assertRaisesRegex(ValueError, "false Rust historical authority"):
            self.guard(report.replace("NO_RUNTIME_ADMISSION", "RUNTIME_ADMITTED"), audit, checklist)

    def test_42_rust_old_ipc_or_wal_never_closes_requirements(self):
        report = self.REPORT.read_text(encoding="utf-8")
        audit = self.AUDIT.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        for task in ("M32-007", "M32-050", "M32-078"):
            with self.subTest(task=task), self.assertRaisesRegex(
                    ValueError, "false Rust checklist closure"):
                self.guard(report, audit, checklist.replace(f"- [ ] **{task}**",
                                                             f"- [x] **{task}**"))

if __name__ == "__main__":
    unittest.main()
