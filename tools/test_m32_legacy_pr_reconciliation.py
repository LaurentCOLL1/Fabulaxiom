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
        # Twelve scoped closures include M32-005 and M32-006 documentary scopes.
        # M32-007 and all runtime gates remain open.
        # Neither historical #35/#215 sources, Linux distribution nor R1-R9 writer are admitted.
        actual_closed = {task for state, task in tasks if state == "x"}
        self.assertEqual(actual_closed, {
            "M32-001", "M32-002", "M32-004", "M32-005", "M32-006", "M32-037", "M32-049",
            "M32-051", "M32-094", "M32-095", "M32-096", "M32-104",
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

if __name__ == "__main__":
    unittest.main()
