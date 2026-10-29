# M3.2 v7 — D3b Windows CI disposable crash/restart refusal, not recovery

**28 October 2026 — owner explicitly authorizes D3b** following the exact-head D3a proof in draft [PR #215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215). This authorization is interpreted within the previous Windows CI-only, per-test fresh disposable fixtures boundary: **no operator data, no production writer activation, no existing-profile SQLite reopen, no marker and no recovery.** It does permit terminating a *child of the CI Rust test binary*, never the app, user session, runner, or operator process.

## Bound exact-source evidence and decision

- Protected `main=90142d8c78dd8a84ee3f0ee1676a753c8521d78e`, PR #214 terminal, independent [postmain #40715995392](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40715995392) SUCCESS. `Protect main` active strict Windows check/no bypass; PR #215 stays **OPEN/DRAFT** with no merge or postmain.
- Previous qualified **D3a exact source** `a7323ab80f12372aa83b2be48019806be212eb32`, [Windows CI #40764117809](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40764117809) SUCCESS, **220/220 Rust, 7/7 Greenfield, 41/41 SQLite guards, 151/151 continuity contracts**; [#38 append-only D3a evidence](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6480242784). Historical success **does not qualify the new D3b SHA**.
- New D3b candidate: **224 Rust / 7 Greenfield / 41 SQLite guards / 152 continuity contracts EXPECTED, NOT QUALIFIED until exact Windows CI at the new PR source SHA**. Four new Rust test functions include one child-only helper; parent run contributes three refusal witnesses. No new CI claim is made by writing this document.
- Threat assumption remains same Windows SID peers trusted/cooperative, not malicious-peer exclusion. P1 one Rust-owned session actor is **selected only**, not activated; P2 deferred. A0 cross-process `EXISTING_PROFILE` admission **STOP**, all R1–R9 production **NOT_PROVEN**.

## Fixture and refusal oracles

Only `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`, already imported through `#[cfg(all(test, windows))]`, adds D3b Rust behavior. The parent creates a **brand-new directory under its CI `%TEMP%`** using `DisposableRoot`, creates the brand-new `new.sqlite3` using `create_new(true)`, and verifies its actual Win32 full FileId128. The child runs that **same current CI test executable** with `--exact` and explicit test-only environment variables, rechecks temp-root naming/file existence, creates a random `Local\Fabulaxiom-D3b-Disposable-…` cooperative mutex, uses the existing test-only D3a VFS and delegated-handle identity vetting, and writes **fiction-only** WAL-mode rows. On the prescribed phase it calls Win32 `TerminateProcess(GetCurrentProcess(), 77)` without `Connection::close()`, Rust Drop, xShmUnmap or explicit mutex release. The parent waits for **exact exit status 77**, inspects only **owned filesystem metadata/FileId128**, and deliberately **never reopens SQLite** on this crashed file. Fixture cleanup happens only after child termination, under the owned temp directory (never individual live WAL deletion).

| Exact Rust test | Observable evidence on Windows CI | Fail-closed decision / unproved property |
|---|---|---|
| `m32_d3b_child_fixture_terminate_before_sqlite_close` | Guarded child helper: committed or pending fiction-only WAL; force termination exit 77 before SQLite close | A helper invoked without its fixture-specific env immediately returns. This is a process-kill simulation, **not power loss or disk durability**. |
| `m32_d3b_committed_wal_abandoned_mutex_refuses_unattested_reopen` | Parent retains an OS handle to child's named mutex but does not own it. After child commits and dies, parent observes `WAIT_ABANDONED`, matching main FileId128 and non-empty WAL | `RECOVERY_REQUIRED_NOT_AUTHORIZED`; **no SQLite reopen**, no successor writer token, no checkpoint/repair. |
| `m32_d3b_pending_wal_vanished_mutex_still_refuses_unattested_reopen` | Child has the **last** mutex handle, dies with pending `BEGIN IMMEDIATE` transaction; parent subsequently creates an **apparently fresh, free** mutex while owned WAL still exists | Same `RECOVERY_REQUIRED_NOT_AUTHORIZED` even with `WAIT_OBJECT_0`. Free mutex **does not attest clean close** or committed/uncommitted fate. |
| `m32_d3b_busy_close_does_not_attest_restart_even_after_final_close` | In a separate owned fresh SQLite fixture, `sqlite3_close` with a live statement returns `SQLITE_BUSY`, while the mutex is held. After statement finalization an explicit close succeeds | BUSY is never a completed-close attestation; later local clean close still does not establish durable cross-process predecessor lineage. `sqlite3_close_v2` delayed destruction is **not exercised**. |

### Strict boundary and negative-result interpretation

1. **D3b is a refusal proof, not recovery proof.** SQLite WAL can contain committed transactions across crash and can reconstruct state upon opening. No survivor invokes rusqlite/SQLite on the crashed path; no SQLite recovery, checkpoint, `PRAGMA`, WAL replay, deletion/rename, repair, status/backup/restore, operator `-wal` or `-shm` access, or existing-profile admission is permitted.
2. A named Win32 mutex is destroyed when the last handle closes. `WAIT_ABANDONED` only remains observable if another process retains an OS handle. The vanished branch demonstrates the dangerous absence of that signal. The synthetic refusal is intentionally unconditional because **there is no authenticated durable predecessor witness**. A replay/swap/omission marker test (D3b-4 in the design) is **not implemented**; durable witness format and production recovery need **separate explicit owner authorization**.
3. `TerminateProcess` causes an abrupt process exit but is not a full machine/power-loss simulation, storage flush proof, WAL frame authentication, exact crash-phase matrix, or verified SHM backing FileId128. xShmUnmap and checkpoint failure injection, `sqlite3_close_v2` deferred-resource behavior, resume of a committed or pending transaction and OS-open atomicity remain unproved.
4. Two newly reviewed Windows-test-only `Connection::open_with_flags_and_vfs` call sites and two `SQLITE_OPEN_READ_WRITE` flags in this same file change the whole-tree inventory tuple **(20,0,0,0,0,21,0) → (22,0,0,0,0,23,0)**. VFS Rust test functions **22 → 26**, whole-tree source inventory and unknown-open tripwires remain enforced. No production Rust module, Tauri command, actor/writer admission, IPC, migration 007, marker, app path or Ollama integration is edited.
5. Confirm exact GitHub PR HEAD, `Protect main`, no unexpected changed files/review threads; exact source CI Windows run must show **224/7/41/152** and all four D3b test names individually pass before calling these *limited CI witnesses* qualified. Old D3a run and any failed candidates are non-transferable. #38 evidence must be **append-only**. PR #215 is a draft and must not be merged under this authorization.

## STOP and downstream product direction

**Production remains unchanged:** writer `NOT_PROVEN`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, real G3 `STOP_UNAVAILABLE`, historical `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 `OPEN/DRAFT`. S3/S4, operator SQLite v6/v7, ACL/backups/journals/sidecars, durable marker, new IPC/CRUD, 007, Windows Hello native and model runtime **STOP**.

Future local Ollama creation models may only receive an **in-memory source-cited, revision-pinned NarrativeContextPacket** (fiches, chronology, histories, canon, character knowledge, reader-reveal horizon) from the single authorized Rust owner after independent gates; no direct database/SQL/writer access, no implicit cloud fallback, human `APPROVE_CANON` for proposed facts. D3b authorizes none of this implementation.

## Primary platform sources

- [Microsoft — TerminateProcess and explicit process-exit wait](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft — Mutex Objects and abandoned-state caveats](https://learn.microsoft.com/en-us/windows/win32/sync/mutex-objects)
- [Microsoft — OpenMutexW, last-handle lifetime](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-openmutexw)
- [SQLite — WAL durability, checkpoint and crash lifecycle](https://www.sqlite.org/wal.html)
- [SQLite — sqlite3_close and sqlite3_close_v2](https://www.sqlite.org/c3ref/close.html)
- [SQLite — io_methods and xShm* callbacks](https://www.sqlite.org/c3ref/io_methods.html)
