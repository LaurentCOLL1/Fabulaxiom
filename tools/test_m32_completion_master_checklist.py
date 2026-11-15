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

if __name__ == "__main__":
    unittest.main()
