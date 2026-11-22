"""No-I/O M3.2 checklist contracts: no operator data, SQLite, network or writer."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md"
SHORT = ROOT / "docs/continuity/RESUME_PROMPT_SHORT.md"
LONG = ROOT / "docs/continuity/RESUME_PROMPT.md"
TASK = re.compile(r"^- \[([ x])\] \*\*(M32-\d{3})\*\*", re.M)


class M32MasterChecklistContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = MASTER.read_text(encoding="utf-8")
        cls.tasks = list(TASK.finditer(cls.content))

    def test_01_104_distinct_tasks_in_order(self):
        self.assertEqual([m.group(2) for m in self.tasks],
                         [f"M32-{n:03d}" for n in range(1, 105)])

    def test_02_visible_numbers_match_exact_checkboxes(self):
        closed = sum(x.group(1) == "x" for x in self.tasks)
        opened = sum(x.group(1) == " " for x in self.tasks)
        self.assertEqual(closed + opened, 104)
        self.assertRegex(self.content, rf"104 tâches identifiées : {closed} clôturées")
        self.assertIn(f"{opened} encore ouvertes", self.content)

    def test_03_checked_tasks_have_dated_scoped_qualification(self):
        for i, m in enumerate(self.tasks):
            if m.group(1) != "x":
                continue
            end = self.tasks[i + 1].start() if i + 1 < len(self.tasks) else len(self.content)
            entry = self.content[m.start():end]
            with self.subTest(task=m.group(2)):
                self.assertIn("**Preuve de clôture :**", entry)
                self.assertIn("**Acquis", entry)
                self.assertRegex(entry, r"2026-11-\d{2}")
                self.assertRegex(entry, r"[0-9a-f]{40}")
                self.assertRegex(entry, r"#[0-9]{7,}")

    def test_04_live_safety_and_final_admission_still_unchecked(self):
        for number in (9, 11, 16, 20, 31, 39, 42, 97, 103):
            self.assertIn(f"- [ ] **M32-{number:03d}**", self.content)
        for marker in ("IN_PROGRESS_NOT_ACCEPTED", "NOT_PROVEN",
                       "STOP_UNAVAILABLE", "PENDING_EXTERNAL_ATTESTATION(21/3/2)",
                       "OPEN_NOT_REMEDIATED", "PRODUCT_FIRST_PARALLEL_SAFETY"):
            self.assertIn(marker, self.content)

    def test_05_both_resumes_link_master_checklist(self):
        for doc in (SHORT, LONG):
            with self.subTest(file=doc.name):
                content = doc.read_text(encoding="utf-8")
                self.assertIn(MASTER.name, content)
                self.assertIn("main=", content)
                self.assertIn("expected_head_sha", content)
        self.assertLess(len(SHORT.read_bytes()), 3600)

    def test_06_next_validation_requires_checklist_update(self):
        for marker in ("Chaque PR matérielle", "date", "SHA",
                       "compteurs", "preuve", "104"):
            self.assertIn(marker, self.content)
        self.assertIn("M32-002", self.content)
        self.assertIn("#42751838279", self.content)
        self.assertIn("#42754285833", self.content)



# M32-004: source-only latest dated checkpoint consistency. No runtime authority.
import json
CHECKPOINT_LEADS=(
 "docs/continuity/RESUME_PROMPT.md", "docs/continuity/HANDOFF_CURRENT.md",
 "docs/continuity/HANDOFF_HISTORY.md", "docs/continuity/M3_2_GATE_DECISION_CURRENT.md",
 "docs/continuity/STATE.md", "docs/continuity/NEXT.md",
 "docs/continuity/M3_2_COMPLETION_MASTER_CHECKLIST_20261109.md",
 "docs/roadmap/ROADMAP_STATUS_CURRENT.md",
)
def guard_checkpoint(short,entry,leads,checklist):
    match=re.search(r"(?m)^main=([0-9a-f]{40})\s*;[^\n]*postmain #(\d+)",short)
    if not match: raise ValueError("STOP short malformed")
    sha,run=match.group(1),int(match.group(2))
    if entry.get("parent_main")!=sha: raise ValueError("STOP parent mismatch")
    post=[v for k,v in entry.items() if k.endswith("_postmain_run") and isinstance(v,int)]
    if post!=[run]: raise ValueError("STOP postmain mismatch")
    if entry.get("gate")!="IN_PROGRESS_NOT_ACCEPTED" or entry.get("strategy")!="PRODUCT_FIRST_PARALLEL_SAFETY":
        raise ValueError("STOP gate promotion")
    if "G3 STOP_UNAVAILABLE" not in short: raise ValueError("STOP short authority")
    rows=re.findall(r"(?m)^- \[([ x])\] \*\*(M32-\d{3})\*\*",checklist)
    if [id for _,id in rows]!=[f"M32-{i:03d}" for i in range(1,105)]:
        raise ValueError("STOP checklist IDs")
    closed=sum(s=="x" for s,_ in rows)
    if entry.get("closed")!=closed or entry.get("open")!=104-closed:
        raise ValueError("STOP counter drift")
    for path,head in leads.items():
        if sha not in head or f"#{run}" not in head:
            raise ValueError("STOP stale lead "+path)
        if not all(x in head for x in ("IN_PROGRESS_NOT_ACCEPTED","G3 STOP_UNAVAILABLE","PRODUCT_FIRST_PARALLEL_SAFETY")):
            raise ValueError("STOP authority drift "+path)

    # Literal source-only STOP gates may not be lost while advancing checkpoints.
    for path, text in (("RESUME_PROMPT_SHORT.md", short), *leads.items()):
        for marker in ("R3 partiel", "D3c conception", "live SQLite WAL-index",
                       "G3 STOP_UNAVAILABLE", "R1–R9 NOT_PROVEN"):
            if marker not in text:
                raise ValueError("STOP safety boundary drift " + path + " " + marker)
    return sha,run,closed
class M32CrossFileCoherence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.short=SHORT.read_text(encoding="utf-8")
        cls.checklist=MASTER.read_text(encoding="utf-8")
        data=json.loads((ROOT/"docs/continuity/HANDOFF_CURRENT.json").read_text(encoding="utf-8"))
        cls.key=next(iter(data));cls.entry=data[cls.key]
        cls.heads={p:(ROOT/p).read_text(encoding="utf-8").split("\n\n",1)[0]
                   for p in CHECKPOINT_LEADS}
    def test_07_eight_document_checkpoint_coherent(self):
        self.assertTrue(self.key.startswith("m32_"))
        sha,run,done=guard_checkpoint(self.short,self.entry,self.heads,self.checklist)
        self.assertRegex(sha,r"^[0-9a-f]{40}$")
        self.assertGreater(run,0)
        self.assertEqual(done+self.entry["open"],104)
    def test_08_stale_short_sha_refused(self):
        text=re.sub(r"(?m)^main=[0-9a-f]{40}","main="+"f"*40,self.short,count=1)
        with self.assertRaisesRegex(ValueError,"parent mismatch"):
            guard_checkpoint(text,self.entry,self.heads,self.checklist)
    def test_09_mismatched_postmain_run_refused(self):
        text=re.sub(r"postmain #(\d+)",lambda m:f"postmain #{int(m.group(1))+1}",self.short,count=1)
        with self.assertRaisesRegex(ValueError,"postmain mismatch"):
            guard_checkpoint(text,self.entry,self.heads,self.checklist)
    def test_10_stale_next_refused(self):
        heads=dict(self.heads);key="docs/continuity/NEXT.md"
        heads[key]=heads[key].replace(self.entry["parent_main"],"0"*40)
        with self.assertRaisesRegex(ValueError,"stale lead"):
            guard_checkpoint(self.short,self.entry,heads,self.checklist)
    def test_11_false_closure_or_gate_refused(self):
        fake={**self.entry,"closed":self.entry["closed"]+1}
        with self.assertRaisesRegex(ValueError,"counter drift"):
            guard_checkpoint(self.short,fake,self.heads,self.checklist)
        fake={**self.entry,"gate":"ACCEPTED"}
        with self.assertRaisesRegex(ValueError,"gate promotion"):
            guard_checkpoint(self.short,fake,self.heads,self.checklist)


# M32-005: reject status/date drift. These tests check source claims, never
# authenticate GitHub's live run status or accept a writer/operator gate.
from datetime import date

def guard_dated_status(short, entry, leads, checklist):
    sha, run, closed = guard_checkpoint(short, entry, leads, checklist)
    try:
        day = date.fromisoformat(entry["date"])
    except (TypeError, KeyError, ValueError) as exc:
        raise ValueError("STOP invalid checkpoint date") from exc
    stamp = day.strftime("%d/%m/%Y")
    line = next((line for line in short.splitlines() if line.startswith("main=")), "")
    if f"date={day.isoformat()}" not in line:
        raise ValueError("STOP short date drift")
    for path, lead in leads.items():
        if not lead.startswith(f"**{stamp} — "):
            raise ValueError("STOP checkpoint date drift " + path)
    if f"{closed}/{104-closed}" not in line:
        raise ValueError("STOP short count drift")
    if entry.get("current_phase") != "SOURCE_ONLY_CANDIDATE_UNQUALIFIED":
        raise ValueError("STOP candidate phase promotion")
    if entry.get("writer_admitted") is not False or entry.get("operator_accepted") is not False:
        raise ValueError("STOP false operator or writer admission")
    if entry.get("source_ci_status") != "COMPLETED_SUCCESS_EXACT_HEAD":
        raise ValueError("STOP source CI claim")
    source_head = entry.get("source_ci_head")
    source_run = entry.get("source_ci_run")
    if not isinstance(source_head, str) or not re.fullmatch(r"[0-9a-f]{40}", source_head):
        raise ValueError("STOP source SHA malformed")
    if type(source_run) is not int or source_run <= 0:
        raise ValueError("STOP source CI run malformed")
    if f"CI #{source_run} PASS" not in line:
        raise ValueError("STOP source CI unlinked")
    for path, lead in leads.items():
        if source_head not in lead or f"#{source_run}" not in lead:
            raise ValueError("STOP source CI proof drift " + path)
    post_state = entry.get("parent_postmain_status")
    if post_state == "PENDING_UNQUALIFIED":
        if f"postmain #{run} PENDING" not in line:
            raise ValueError("STOP pending CI portrayed as success")
    elif post_state == "COMPLETED_SUCCESS_EXACT_MAIN":
        if entry.get("attested_postmain_sha") != sha or f"postmain #{run} PASS" not in line:
            raise ValueError("STOP postmain success without same SHA attestation")
    else:
        raise ValueError("STOP postmain status unrecognized")
    return sha, run, closed

class M32DatedStatusTruth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.short=SHORT.read_text(encoding="utf-8")
        cls.checklist=MASTER.read_text(encoding="utf-8")
        data=json.loads((ROOT/"docs/continuity/HANDOFF_CURRENT.json").read_text(encoding="utf-8"))
        cls.entry=next(iter(data.values()))
        cls.leads={p:(ROOT/p).read_text(encoding="utf-8").split("\n\n",1)[0]
                   for p in CHECKPOINT_LEADS}

    def test_12_current_date_and_evidence_status_consistent(self):
        sha,run,closed=guard_dated_status(self.short,self.entry,self.leads,self.checklist)
        self.assertRegex(sha,r"^[0-9a-f]{40}$")
        self.assertGreater(run,0)
        self.assertEqual(closed,13)

    def test_13_falsified_or_stale_date_refused(self):
        bad=dict(self.entry,date="2026-11-12")
        with self.assertRaisesRegex(ValueError,"date drift"):
            guard_dated_status(self.short,bad,self.leads,self.checklist)
        with self.assertRaisesRegex(ValueError,"short date drift"):
            guard_dated_status(self.short.replace(f"date={self.entry['date']}","date=2026-11-12"),
                               self.entry,self.leads,self.checklist)

    def test_14_unattested_success_refused(self):
        forged=dict(self.entry,parent_postmain_status="COMPLETED_SUCCESS_EXACT_MAIN",
                    attested_postmain_sha="0"*40)
        with self.assertRaisesRegex(ValueError,"postmain success without"):
            guard_dated_status(self.short,forged,self.leads,self.checklist)

    def test_15_false_writer_operator_or_gate_promotion_refused(self):
        for patch in ({"writer_admitted":True},{"operator_accepted":True},
                      {"current_phase":"ACCEPTED"},{"gate":"ACCEPTED"}):
            with self.subTest(patch=patch),self.assertRaisesRegex(ValueError,
                    "admission|promotion"):
                guard_dated_status(self.short,{**self.entry,**patch},
                                   self.leads,self.checklist)

    def test_16_forged_source_ci_proof_refused(self):
        with self.assertRaisesRegex(ValueError,"source CI proof drift"):
            guard_dated_status(self.short,{**self.entry,"source_ci_head":"a"*40},
                               self.leads,self.checklist)
        with self.assertRaisesRegex(ValueError,"source CI unlinked"):
            guard_dated_status(self.short,{**self.entry,"source_ci_run":99999999999},
                               self.leads,self.checklist)

    def test_17_false_short_counter_or_source_outcome_refused(self):
        with self.assertRaisesRegex(ValueError,"short count drift"):
            guard_dated_status(self.short.replace("13/91","12/92",1),
                               self.entry,self.leads,self.checklist)
        with self.assertRaisesRegex(ValueError,"source CI claim"):
            guard_dated_status(self.short,{**self.entry,
                               "source_ci_status":"PENDING_UNQUALIFIED"},
                               self.leads,self.checklist)

    def test_18_missing_safety_boundary_in_resume_or_lead_refused(self):
        bad_short = self.short.replace("R3 partiel", "R3 absent", 1)
        with self.assertRaisesRegex(ValueError, "safety boundary drift"):
            guard_dated_status(bad_short, self.entry, self.leads, self.checklist)
        bad_leads = dict(self.leads)
        p = "docs/continuity/NEXT.md"
        bad_leads[p] = bad_leads[p].replace("D3c conception", "D3c absent", 1)
        with self.assertRaisesRegex(ValueError, "safety boundary drift"):
            guard_dated_status(self.short, self.entry, bad_leads, self.checklist)
        bad_leads = dict(self.leads)
        p = "docs/continuity/RESUME_PROMPT.md"
        bad_leads[p] = bad_leads[p].replace("live SQLite WAL-index", "WAL sans garde", 1)
        with self.assertRaisesRegex(ValueError, "safety boundary drift"):
            guard_dated_status(self.short, self.entry, bad_leads, self.checklist)


    def test_19_old_dated_handoff_checkpoint_preserved(self):
        """Previous dated record stays in document history, never retroactively updated."""
        marker = ("**20/11/2026 — PR #399 P3bd FUSIONNÉE CI/POSTMAIN PASS ; "
                  "P3be FILTRE SCÈNE SOURCE HISTORIQUE FICTIVE CANDIDAT.**")
        for path in CHECKPOINT_LEADS:
            with self.subTest(path=path):
                doc=(ROOT/path).read_text(encoding="utf-8")
                self.assertEqual(doc.count(marker),1)
                old_header=doc.split(marker,1)[1].split("\n\n",1)[0]
                self.assertIn("c1c3f5489cd69bcd86c6022ce7a559d2c5c7ac83",old_header)
                self.assertIn("#44769664255",old_header)
                self.assertGreater(doc.index(marker),doc.index("\n\n"))

    def test_20_pending_postmain_not_pass_and_writer_still_refused(self):
        """Invert the actual dated status; never treat pending as success or vice versa."""
        state=self.entry["parent_postmain_status"]
        if state=="PENDING_UNQUALIFIED":
            fake={**self.entry,"parent_postmain_status":"COMPLETED_SUCCESS_EXACT_MAIN",
                  "attested_postmain_sha":self.entry["parent_main"]}
            expected="postmain success without same SHA attestation"
        elif state=="COMPLETED_SUCCESS_EXACT_MAIN":
            fake={**self.entry,"parent_postmain_status":"PENDING_UNQUALIFIED",
                  "attested_postmain_sha":None}
            expected="pending CI portrayed as success"
        else:
            self.fail("STOP unknown postmain state in negative test")
        with self.assertRaisesRegex(ValueError,expected):
            guard_dated_status(self.short,fake,self.leads,self.checklist)
        self.assertEqual(self.entry["gate"],"IN_PROGRESS_NOT_ACCEPTED")
        self.assertIs(self.entry["writer_admitted"],False)
        self.assertIs(self.entry["operator_accepted"],False)


    @staticmethod
    def issue38_scoped_audit_entry():
        """M32-006 belongs to its original dated evidence, not latest handoff."""
        data=json.loads((ROOT/"docs/continuity/HANDOFF_CURRENT.json").read_text(encoding="utf-8"))
        return data["m32_20261120_p3bg_m32_006_candidate_after_pr401"]

    def test_21_issue38_scoped_metadata_audit(self):
        audit=self.issue38_scoped_audit_entry()
        doc=(ROOT/"docs/qualification/M3_2_M32_006_ISSUE38_APPEND_ONLY_SCOPED_AUDIT_20261120.md").read_text(encoding="utf-8")
        for marker in ("737 commentaires accessibles","737 IDs uniques",
                       "#6194801978","#7050753731","#44800008968",
                       "#44800413136","#44818205234","NOT_PROVEN"):
            self.assertIn(marker,doc)
        self.assertIn("- [x] **M32-006**",self.checklist)
        self.assertIn("- [ ] **M32-007**",self.checklist)
        self.assertEqual(audit["m32_006_comment_count"],737)
        self.assertEqual(audit["m32_006_unique_comments"],737)
        self.assertIs(audit["m32_006_historical_deletions_proven_absent"],False)

    def test_22_false_issue38_historical_assertion_refused(self):
        audit=self.issue38_scoped_audit_entry()
        doc=(ROOT/"docs/qualification/M3_2_M32_006_ISSUE38_APPEND_ONLY_SCOPED_AUDIT_20261120.md").read_text(encoding="utf-8")
        def guard(text, entry):
            if "737 commentaires accessibles" not in text or "#7050753731" not in text:
                raise ValueError("STOP journal baseline drift")
            if "#44800008968" not in text or "FAILURE" not in text:
                raise ValueError("STOP failure erased")
            if entry.get("m32_006_historical_deletions_proven_absent") is not False:
                raise ValueError("STOP deletion absence invented")
        guard(doc,audit)
        with self.assertRaisesRegex(ValueError,"baseline drift"):
            guard(doc.replace("737 commentaires accessibles","738 commentaires accessibles"),audit)
        with self.assertRaisesRegex(ValueError,"failure erased"):
            guard(doc.replace("FAILURE","PASS"),audit)
        with self.assertRaisesRegex(ValueError,"deletion absence"):
            guard(doc,{**audit,"m32_006_historical_deletions_proven_absent":True})

if __name__ == "__main__":
    unittest.main()
