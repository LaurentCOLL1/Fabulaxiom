# M3.2 — G2-B → G3 evidence decision after Win32 FileId counterexamples (22 October 2026)

**STATUS: SOURCE-ONLY ARCHITECTURAL EVIDENCE REVIEW. NO WINDOWS OPERATOR PROCEDURE. NO REAL DATABASE ACCESS.** This memo follows protected [PR #133](https://github.com/LaurentCOLL1/Fabulaxiom/pull/133) and [PR #134](https://github.com/LaurentCOLL1/Fabulaxiom/pull/134). It is not an approval, capture runbook or substitute for an independent attestation. It does not modify `docs/qualification/M3_2_G3_SOURCE_ACQUISITION_DECISION.md` and is subordinate to the continuity gate.

## Observed evidence, classified carefully

| Evidence | Owner-reported observation / GitHub lab | What it **cannot** prove |
| --- | --- | --- |
| M1.5 activation selector | One matching restored-v6 candidate and marker; isolated-v7 candidate present | Historical source authenticity; schema version; exclusion of writers |
| NTFS metadata and paths | Three file roles observed; ACL readable; no reparse points or sidecar names reported; sizes/timestamps equal across two reads | Continuous quiescence; file content integrity; absence of hot journals outside the observed names/time |
| FileIdInfo | Three files and ancestor handles checked twice with `FILE_READ_ATTRIBUTES`, `FILE_SHARE_READ|WRITE|DELETE` | No concurrent writer, no replacement after handle release, external provenance |
| CI scratch counterexamples | Test 06 demonstrates **same volume and FileId with changed bytes** under `SHARE_ALL`; test 08 shows `FILE_READ_ATTRIBUTES / SHARE_READ` still permits a `GENERIC_WRITE` opening on disposable Windows bytes | Any state of real production SQLite or a feasible exclusive capture policy |
| Existing owner-to-RAM toy | `tools/m3_2_g3_owned_online_backup_toy.py` uses a PRE-EXISTING fictional SQLite owner connection and Online Backup to RAM with validation and a new-only synthetic restore | A pre-existing trusted owner connection in real Fabulaxiom, real source provenance, permission to start/open original |

All local observations are **owner-reported, sanitized and not independently attested**. No private paths, volume IDs, FileId values, original hashes, marker contents or database records are published to GitHub.

## Decision matrix — no automatic route

| Strategy | Verified prerequisite | Current disposition |
| --- | --- | --- |
| Existing trusted owner connection + SQLite Online Backup → RAM | Existing authentic, non-migrating SQLite owner handle bound to the exact original and safe owner lifecycle; memory, validation and private destination review | **UNAVAILABLE / NOT PROVEN** in current real runtime; no new SQLite open just to create the handle |
| Cold source with retained identity and resolved transaction state | Independent custody, ancestor/path identity, continuous writer exclusion, WAL/rollback/hot-journal accounting, safe source read, no recovery writes | **NOT PROVEN**; no cold copy or raw-byte capture |
| General `open_database`, `database_status`, M1.5 create/restore backup commands | Would require new audited entrypoint rather than existing potentially migrating or replacing calls | **VETO** for protected originals |
| Raw copy, `mode=ro`, `immutable=1`, FileId/timestamp/hash-only acquisition | No guarantee of coherent transaction state and authentic isolated provenance | **VETO**; never treat apparent read-only as sufficient |
| Synthetic Online Backup or Win32 tests | Controlled invented fixture only | **VALID FOR LABORATORY NEGATIVE/POSITIVE TESTS ONLY**, never proof of operator custody |

SQLite's Online Backup API can yield a transactionally consistent destination despite updates by other clients; it locks the source only during reads and may restart internally. It does **not** require proving that no writer exists, but it **does require** a trusted already-open source connection and a safe plan to acquire it. This project currently has no proven real non-migrating owner connection; no shortcut to G3 follows from the API's guarantees. A fresh destination can otherwise be overwritten by generic backup APIs, so output publication remains a distinct safety boundary.

See [SQLite Backup API](https://www.sqlite.org/backup.html) and [C API backup semantics](https://www.sqlite.org/c3ref/backup_finish.html). For `FILE_READ_ATTRIBUTES` sharing caveats see [Microsoft CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).

## Precise evidence that would be needed for a separate proposal

1. Independent provenance for the exact historical files and marker and an authenticated link between recorded source and the current handle. Historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)` is still unresolved.
2. A **demonstrated** non-migrating owner acquisition route already present before any capture, **or** independently proven exclusive cold custody with complete SQLite journal state. If neither exists, the gate result is **STOP**.
3. A source-only and synthetic negative matrix for busy, replaced, vanished, stale and writer-conflicted source, interrupted backup, destination collision, capacity/ACL failure and snapshot validation; never silently fall back to raw copy.
4. A new-only private destination, explicit restore and validation on an isolated *third* copy. Do not conflate v6 and isolated v7 as a transactionally atomic pair.
5. A fresh exact-script operator review and approval for *each* private path and proposed side effect, including any attempted SQL opening, lock, writing, process interaction, `q`, UAC or failure case. A general `Continue` is not authorization.

**Current terminal decision:** `G2B_GLOBAL=NOT_ACCEPTED`; `SOURCE_AUTHENTICATION=PARTIAL_LOCAL_IDENTITY_ONLY`; `SQLITE_WRITER_ABSENCE=NOT_PROVEN`; `G2C=NOT_AUTHORIZED`; `G3_REAL=STOP_UNAVAILABLE`; `M3.2=IN_PROGRESS_NOT_ACCEPTED`. No G2C hash, real SQL read, G3 snapshot, migration 007, IPC writer, M3.3, ComfyUI or release. The active v6, isolated v7, sidecars, backups, ACL and marker remain untouched.

## Exact GitHub handoff chronology

- PR #133 source head `d2bf3134054c4f1a05432c51055134fec7b4a0b2`; source [CI #39835840939](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39835840939) SUCCESS; protected merged `604817c8457aaf7136f587aaaff28ff862e2702a`. Earlier failed #39835364262 preserved as negative evidence.
- PR #134 source head `f0db9b28d0e8492f3bc64c952b722873ae61311e`; source [CI #39837909918](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39837909918) SUCCESS; protected merged `a1185b8345999f10814fd54dab96890f70236a5c`; exact post-main [CI #39839580270](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39839580270) completed/SUCCESS.
- PR #133 post-main CI #39837202639 completed/SUCCESS is a **later separate observation**; its original `IN_PROGRESS_AT_CHECKPOINT` object must remain historically intact. The same principle applies to each prior dated checkpoint.
