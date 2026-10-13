# M3.2 Stage 18 — Independent isolated M3.1 v7 SQLite physical read-only gate

**NEW SOURCE CANDIDATE — exact-head Windows CI NOT YET QUALIFIED. NO REAL OPERATOR EXECUTION AUTHORIZED.**

## Baseline and evidence

At PR #35 HEAD `281d6667b5d08ca0ab3217d24e650574bc70f2ca`, the required Windows pull_request [run #38421108816](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38421108816) is completed/success, 29/29 job steps. The operator subsequently ran Stage 17 on the live PC from the clean, detached fifth worktree `M:\Fabulaxiom-M32-audit-281d6667` using explicit `C:\Python\Python312\python.exe -B`: **4/4 custody roots, 26/26 roles, 21/21 historical source pins and 3/3 recent observations MATCH; 2 roles remain unanchored.** The tool returned exactly `PENDING_EXTERNAL_ATTESTATION` / exit code 2, and both main and M3.2 worktrees remained clean. This is byte custody only, not SQLite physical integrity and not historical ACL notarization.

## Stage-18 source candidate

`tools/m3_2_isolated_v7_physical_readonly.py` provides an additional, **opt-in `--dry-run` only** physical inspection of the **existing independently preserved M3.1 isolated candidate v7**, specifically `%LOCALAPPDATA%\com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd\database\fabulaxiom.sqlite3`. It NEVER opens the restored-active **production v6**. Before any SQLite connection it invokes Stage 17's full four-root 26-role source-anchored SHA/sidecar/activation/medium-token/Git gate and requires `PENDING_EXTERNAL_ATTESTATION`. The isolated copy must still match the source-pinned SHA-256 `566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402`.

The physical checker rejects symlinks/junctions/reparse points, missing/oversized file, SQLite invalid header or WAL-mode header, and any `-wal`, `-shm` or `-journal` sidecar **before opening** a connection. It compares the source file's SHA-256 and stat identity before/after. For rollback-journal-mode only, it opens `file.as_uri() + '?mode=ro&cache=private'`, SQLite connection timeout 0, sets `PRAGMA query_only=ON`, foreign keys ON, and `PRAGMA temp_store=MEMORY`; no `immutable=1` because that disables normal file-change detection.

The source-only read pass requires exactly seven migration rows with the M3.1 v7 candidate named `007_create_world_time_foundation`, schema owner `fabulaxiom`, `PRAGMA integrity_check = ok` and **separately** zero `PRAGMA foreign_key_check` violations. It checks all fourteen original v6 and all three candidate world-time tables are STRICT, requires all three candidate tables empty, and recomputes the historical typed-v1 combined legacy logical SHA `38a610da9d6d9fcaa7842ebcbfa4f2c644d892c7968797de5f9ba21a258b2269`. SQLite closes before final file/sidecar SHA/identity revalidation. Positive inspection still means `PENDING_EXTERNAL_ATTESTATION`, never READY, and the CLI always exits 2.

## Synthetic-only CI

`tools/test_m3_2_isolated_v7_physical_readonly.py` adds 16 synthetic tests. Fixtures are newly constructed **disposable** SQLite databases in temp folders and explicit-close connection contexts. They test: valid complete v7 scan and unchanged bytes, SHA mismatch before open, typed-legacy digest mismatch, modified or missing migration row, wrong schema owner, FK violation that `integrity_check` alone would miss, missing/non-STRICT candidate table, nonempty candidate table, WAL sidecar preservation, WAL header refusal, bad SQLite header, a changing SHA during scan, rejection before SQLite on failed parent gate, and strict pending-only integration. New Windows workflow step runs these fixtures only; it never mounts or reads the operator's original files.

## Safety / remaining blocks

**No operator invocation of this new Stage 18 script is authorized until a new exact-HEAD Windows CI passes and a separate non-admin Windows command is reviewed.** The operator stopped-app ACK is an assertion; it does not itself prove absence of all possible external writers. SHA/stat bracketing detects many races but is not an OS-enforced immutable snapshot. The earlier M3.1 physical third-copy test is useful supporting evidence, not a substitute for fresh Stage-18 acceptance on the isolated M3.1 copy. The 2 unanchored files and independent provenance for the 2 ACL archives/early M2.4 manifest remain unresolved. No release, no registration of migration 007 for normal startup, no new M3.2 writable identity/IPC, no modification of production SQLite v6, no PR merge or M3.3. Keep PR #35 DRAFT.

SQLite authoritative references: https://www.sqlite.org/uri.html ; https://www.sqlite.org/pragma.html ; https://www.sqlite.org/wal.html ; https://www.sqlite.org/tempfiles.html .
