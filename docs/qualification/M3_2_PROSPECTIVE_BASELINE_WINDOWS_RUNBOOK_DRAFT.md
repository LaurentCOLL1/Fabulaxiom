# M3.2 — Windows prospective baseline operator runbook (DRAFT ONLY)

**Status: NOT EXECUTABLE / NO LOCAL OPERATIONS AUTHORIZED.** Version: proposal 2026-10-15. Parent authority: [prospective baseline governance decision](M3_2_PROSPECTIVE_TRUST_BASELINE_DECISION.md); historical blocker [issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36). Never paste this file as an automated PowerShell script.

## Purpose and boundary

This is the **review checklist for a future ceremony**, not a command list to run now. It describes which checks an authorized operator and an independent reviewer must perform **after** a separate, exact-head, non-destructive execution plan is approved. The current active M1.5 restored SQLite schema is **v6**; M3.1 v7 exists in an **isolated** copy. The original seven worktrees, databases, manifests, backup chains and ACL files are protected.

No historical role is promoted by this runbook. `PENDING_EXTERNAL_ATTESTATION` remains 21 pinned / 3 observed-only / 2 unanchored. The prospective reference is **NOT_STARTED** and real M3.2 runtime integration remains **NOT_AUTHORIZED**.

## Ceremony preparation (reviewer-approved before starting)

| Check | Required planned evidence | STOP condition |
| --- | --- | --- |
| Exact Git identity | Fresh `main`, PR #35 and proposed operator-plan head SHA, PR/CI status | Changed head, dirty protected source, unqualified plan |
| Windows security | Standard medium-integrity token, approved user SID/ACL scope; no elevation unless separately permitted | Elevated application, ACL drift, unknown permission |
| Process safety | Tauri/Fabulaxiom closed; Ollama state recorded without unapproved process changes; DB read-only feasibility assessed | Writers/processes cannot be excluded safely |
| Custody roots | Seven original worktrees counted and left in place, original manifests, ACL exports, restored v6 and isolated v7 correctly distinguished | Ambiguous path, missing source, role swap |
| Backup integrity | Prior backup SHA/length/roles retained as observational evidence; existing backups never overwritten | Hash conflict, collision, missing original |
| Destination | Distinct previously unused approved private location, permissions, disk space, encryption/retention policy | Destination collision, insufficient capacity |
| Reviewer | Independent named human reviewer or explicitly approved alternative (not self-certified) | Reviewer independence undefined |
| Privacy | Sanitized publication plan; no secrets, private absolute paths or SQLite content in public repo | Public data exposure |

## Proposed sequence, no runnable instructions here

**A. Pre-capture custody observation.** Record original role IDs and file existence, SHA-256/length only where authorization permits, schema and active pointer. Handle WAL/SHM with SQLite's documented mechanisms; do **not** assume a plain copy of an active database file is a valid snapshot. Never run automatic migration 007 or change any original file permissions.

**B. SQLite-consistent prospective snapshots.** Use the [SQLite Online Backup API](https://www.sqlite.org/backup.html) on an approved source for a fresh independent destination. Pin source-role mapping, exact backup-tool version/configuration, time, successful completion and one-to-one output identity. Do not rewrite production SQLite or point the application to the new copy. If a different tool or `VACUUM INTO` is proposed, document semantic differences and approve separately: `VACUUM INTO` creates a logically equivalent compact copy, not necessarily a byte-identical file and may remove deleted traces.

**C. Standalone copy verification.** On the new snapshots only: `integrity_check=ok`, no foreign-key violations, schema `user_version` matching the intended copy's schema, counts and canonical logical digests for protected tables and text-revision ancestry; compare backup metadata to the preflight role inventory. On Windows, after backup, no unexpected sidecar, protected pointer or ACL mutation may be attributed to the ceremony.

**D. New manifest and prospective chain-of-custody.** Produce a freshly versioned, collision-resistant output name, content digests, relative role identifiers, tool/runtime versions, new creation timestamp (never backdated), archive format version, evidence author, reviewer ID and storage location, policy ID and explicit `PROSPECTIVE_FROM` boundary. Cryptographically authenticate the manifest with independently governed keys or custody system; SHA-256 by itself cannot prove authorship. Store protected originals and validated new copies in separately secured locations. Minimize and redact logged content.

**E. Non-destructive restore rehearsal.** Restore only to a separately named isolated empty destination. Verify integrity and foreign keys again, schema/version, row counts, logical digests, declared source provenance, access permissions and application-free read-only audit, with original worktrees and pointers unchanged. Don't trigger migrations, GUI editors or scheduled background processes.

**F. Independent assessment and signed decision.** Reviewer validates original vs new role identity, manifest authenticity, retention, snapshot usefulness, documented gaps and fail-closed results. Mark **new** reference either `ACCEPTED_FOR_FUTURE_REFERENCE` or `REJECTED/INCONCLUSIVE`; never convert the five older roles from `OBSERVED`/`UNANCHORED` to historical pinned. If no independent reviewer, keep a `REVIEW_PENDING` state rather than inventing approval.

**G. Product handoff only after separate permission.** Publish sanitized decision record and future requirements. A new PR must explicitly authorize an isolated read-only Tauri/React candidate and its operator Windows acceptance; never silently use this document to merge PR #35, activate v7 in production or author time events.

## Mandatory safe-open and destination protocol review (still NOT EXECUTABLE)

Before a future operator even **opens** either protected source database, the exact approved plan must state all of the following and obtain separate permission:

1. **Mode verification without touching originals:** identify if the source is in rollback-journal or WAL mode only by a method explicitly shown to cause no protected-file mutation. SQLite may require `-wal`/`-shm` or may create them for a read-only opener. Never assume a readonly connection cannot produce filesystem side effects. Abort if the proposed connection, existing sidecars, locking or access rights are not validated.
2. **Do not force `immutable=1`:** this skips locking/change detection; prohibit it on an active source without independently established actual immutability. Never issue `wal_checkpoint`, set `journal_mode` or delete `-wal`/`-shm` on any original as a preliminary safety shortcut.
3. **Create-new destination guarantee:** reject an existing path, reparse point/junction/symlink, unsafe parent directory, duplicate output name and races. Because the SQLite Backup API **can overwrite the destination**, the implementation needs an independently reviewed exclusive create-new/identity mechanism. Refuse on any uncertainty or reuse; `Test-Path` alone is not sufficient to defeat races.
4. **Separate physical vs logical evidence:** hash every original byte stream that is safely observable, but do **not** assert the source `.sqlite3` digest is equal to a consistent destination snapshot that incorporates WAL changes. Capture the new snapshot digest and separately compare its logical content and schema under a versioned canonicalization; verify the new copy and its independent restoration.
5. **Failure is non-authorizing:** source lock, insufficient permissions, WAL/SHM uncertainty, `SQLITE_BUSY`/`SQLITE_LOCKED`, incomplete backup/close, unexpected file creation, or ambiguous source/destination identity -> STOP. Document only a sanitized failure; do not run automatic repair/checkpoint, reopen with elevated rights or fall back to raw copy.
6. **No cross-database atomicity assumption:** a series of individually consistent SQLite snapshots does not automatically freeze two distinct sources at one instant; record separately validated source/identity/time and require an explicit consistency model before making any cross-copy provenance claim.

Review references: [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite immutable URI](https://www.sqlite.org/uri.html), [SQLite Backup API](https://www.sqlite.org/backup.html), [SQLite PRAGMA](https://www.sqlite.org/pragma.html).

## Proof bundle (private: never upload to public GitHub)

- Source role inventory with digests or scoped absence and exact date, pointer verification, seven-worktree custody, process/token/ACL notes.
- Consistent backup completion and immutable manifest, independent authenticity material, destination digest and byte lengths, scheme for relinking sources without private-path disclosure.
- SQLite integrity and foreign-key outputs, schema/version, canonical table/revision logical digests and backup-and-restoration equivalence.
- Original unchanged postflight checks, independent reviewer findings, explicit authority scope and prospective date.
- Separate historical issue #36: every old role marked still `HISTORICAL_UNVERIFIED` or verified only by genuinely older third-party evidence.

## Acceptance matrix

| Exit state | Meaning | May enable new M3.2 read-only operator testing? |
| --- | --- | --- |
| `NOT_STARTED` | Proposal reviewed or PR CI green, no local work | **No** |
| `PREPARED` | Future authorized plan reviewed, files still untouched | **No** |
| `COLLECTED_UNDER_AUTHORIZATION` | New private backup and manifest captured | **No** |
| `REVIEW_PENDING` | Restoration pending or no independent reviewer | **No** |
| `ACCEPTED_FOR_FUTURE_REFERENCE` | Prospective snapshot authenticated, restore tested and reviewer accepted | **Still no: requires separately authorized read-only M3.2 integration plan** |
| `REJECTED/INCONCLUSIVE` | Safety or verification blocker | **No; repair plan reviewed separately** |

**Unchanged prohibitions:** no protected worktree mutation, no old-file overwrite/delete, no production v6→v7 007, no ACL change without independent permission, no writing IPC, no secret/material publication, no PR #35 merge, no M3.3. A current successful CI is a code qualification, never historical custody proof.
