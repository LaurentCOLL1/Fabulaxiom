# M3.1 — Windows operator v6 safety and third-copy v7 rehearsal evidence

**Recorded:** 2026-10-11 (Europe/Paris). **PR:** #33, candidate exact source `a45d41ceb22641494f4168380839bce45a394085`; exact source CI run **#38122561283** `pull_request completed/success`, 18/18 Windows steps. This document records **operator-reported terminal output**, not access by GitHub CI to the operator workstation.

## Preserved source and prerequisites

- Production M1.5 active restored database remains **SQLite v6**: `fabulaxiom-restored-00000000000001791428210487599800-0000025660-0000000001.sqlite3`.
- Original production closed-file SHA-256: `b904731afac0b6b6135ba6d6a8a8dee3548c50daca1a5ee3a7788db85cee16ff`; typed v1 logical SHA-256: `38a610da9d6d9fcaa7842ebcbfa4f2c644d892c7968797de5f9ba21a258b2269`. All fourteen historic table snapshots PASS. This digest uses `fabulaxiom-v6-typed-row-sha256-v1`; it must not be substituted for earlier M2 logical-digest formats.
- Existing operator-backed historic v3, v4, v5 and *isolated* M2.5 v6 files retain their previously checked SHA-256 custody and manifest integrity. M2.5 isolated fixture contents are not production data.
- Application/Tauri/Ollama closure preflight PASS; prior read-only source v6 audit and new backup `--dry-run` PASS. Manual assertions are not an automated proof of process shutdown.

## Verified additional v6 safety snapshot and restore

- Custody folder (relative to production app data): `operator-qualification/m3_1/pre_v7_20261011T074045Z-88956f2eb16a4503a0d44d0e9bc968ab`.
- `fabulaxiom-pre-m3-1-v6.sqlite3` SHA-256: `b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495`.
- Independent `isolated-restore-rehearsal-v6.sqlite3` SHA-256: same `b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495`.
- `manifest.json` SHA-256: `819abb95ef9147bed6fd13a8189bccf09f97d808a093c1160b4d6e8957b94d59`.
- Operator output: **14/14 legacy tables** and typed historical digest unchanged, original source SHA unchanged, M1.5 pointer unchanged; backup, restored copy and manifest SHA independently matched.

## Third-copy candidate-v7 rehearsal — actual Windows PASS

**Exact Git candidate source:** `a45d41ceb22641494f4168380839bce45a394085`. Operator verified the Git blobs of `tools/m3_1_v6_audit.py`, `tools/m3_1_v6_backup.py`, `tools/m3_1_v7_copy_rehearsal.py` and `src-tauri/sql/m3_1_world_time_v7_candidate.sql`. Candidate SQL SHA-256: `d66c26349e0bbfe0a9b9d610516c6ebe8d241d01f9506d0613f4152d25cd1212`.

- Operator `--dry-run`: `status=READY`, `mode=read_only_copy_rehearsal_dry_run`; backup and manifest digests verified; **no new database** and **no migration**.
- Operator separately executed `--create` on **a newly derived third copy only**, not the source or the preserved backup/restore.
- Rehearsal folder: `operator-qualification/m3_1/v7_copy_rehearsal_20261011T090737Z-d6450d9cd5f34ca4a574bb4a2eb32fd0`.
- Candidate `candidate-v7.sqlite3` SHA-256: `566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402`.
- `candidate-v7-manifest.json` SHA-256: `82da38026dee3002e9726ae1bdb92fb22c6554710f3ce74ab152449563345cc7`.
- `status=PASS`, `mode=v7_copy_only_rehearsal`, `legacy_data_preserved=true`, `production_migrated=false`, `source_unchanged=true`, `active_pointer_modified=false`.
- Operator's separate SQLite read-only verifier: exact version ledger **1–7**, seventh name `007_create_world_time_foundation`, physical integrity **ok**, foreign-key check **empty**, new `fictional_calendars`, `world_time_anchors`, `world_time_precedences` all **STRICT** and **empty**.
- Independent PowerShell hashes for new candidate/manifest both **PASS**. Original production v6, safety backup, v6 restore and original manifest hashes unchanged. Neither production M1.5 pointer nor either preserved M2.5 worktree was modified.

## Remaining governed gates — NOT YET PASS

1. **Operator fourth-copy rollback: PASS**, as independently verified and recorded above.
2. **Independent actual third-copy v7 read-only / RAM temporal audit: PASS**, verified on operator Windows at source HEAD `4c7526f749d758dd33ccb961e67f8a611cd2ff62`, 10/10 scenarios and eight unchanged protected files, as recorded below.
3. **Outstanding:** this new *evidence commit's own exact-head terminal `pull_request` CI PASS**, final fresh scope/main review, and an explicit decision about the roadmap's controlled-launch/post-v7 gate (not yet performed against production).
4. **Outstanding:** only after all governed acceptance criteria may a controlled PR merge and separate post-merge normalization be considered. **Do not automatically register 007 in normal startup, do not upgrade production from v6, and do not authorize M3.2+.**

The real Windows third-copy PASS is **not** a production migration acceptance. SQLite reference: https://www.sqlite.org/backup.html ; https://www.sqlite.org/pragma.html .

## Fourth-copy forced-error rollback — Windows operator PASS

**Date:** 2026-10-11; exact source HEAD `4e01be2e9abb41e2dd9544996d8c59a262454b07`; `pull_request` Windows CI #38133034733, `completed/success`, 19/19 steps. Operator extracted all five Git-verified source files and completed both `--dry-run` (READY, no writes) and separately invoked `--create` on a **new fourth isolated derivative**, not on production or the preserved third v7 copy.

- Fourth directory: `operator-qualification/m3_1/v7_rollback_rehearsal_20261011T111844Z-8e53aaaabae847f2b982b089fc7b7a57`.
- Deliberate error: `SQLITE_CONSTRAINT_PRIMARYKEY` while the candidate SQL was staged inside an open transaction; explicit rollback PASS.
- Rolled-back fourth database SHA-256: `b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495`, exactly equal to the v6 safety backup.
- New rollback manifest SHA-256: `353170fa726b743bd810867e612acf4ecc0530ceca2268a7a53fda92145a6b0f`.
- Independent read-only SQLite verifier: six historic migration rows, all 14 table digests, entire historical DDL inventory, physical integrity and foreign keys PASS; no candidate v7 tables remain.
- Original active v6 database, protected v6 safety backup, v6 restore, manifest, successful third v7 copy and third-copy manifest SHA-256 all MATCH before and after; active M1.5 pointer unchanged.

**Disposition:** operator rollback gate is PASS for the fourth disposable copy. This does not constitute a production upgrade, live app-startup v7 test or permission to register migration 007.

## Final read-only v7 audit of preserved third copy — actual operator Windows PASS

**Source/CI:** operator executed the Git-blob-verified `tools/m3_1_v7_final_readonly.py` from exact source HEAD `4c7526f749d758dd33ccb961e67f8a611cd2ff62` after `pull_request` Windows CI **#38139894514 completed/success, 20/20 steps** (11+9+8+6+6 Python fixture tests and 99 Rust tests successful). Actual candidate SQL SHA-256 **`d66c26349e0bbfe0a9b9d610516c6ebe8d241d01f9506d0613f4152d25cd1212`**.

The operator verified eight protected artifacts *before and after* the audit, all SHA-256 MATCH:
- Restored-active production v6: `b904731afac0b6b6135ba6d6a8a8dee3548c50daca1a5ee3a7788db85cee16ff`.
- Safety v6 backup and separate v6 restore: `b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495` each.
- Safety v6 manifest: `819abb95ef9147bed6fd13a8189bccf09f97d808a093c1160b4d6e8957b94d59`.
- Preserved third candidate v7: `566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402`.
- Third v7 manifest: `82da38026dee3002e9726ae1bdb92fb22c6554710f3ce74ab152449563345cc7`.
- Fourth copy rolled back to v6: `b2059574929e06d9966cce96df97b4f3337d0f7b56afa5734a862110af00d495`.
- Fourth rollback manifest: `353170fa726b743bd810867e612acf4ecc0530ceca2268a7a53fda92145a6b0f`.

**Actual tool JSON:** `status=PASS`, `mode=third_copy_read_only_plus_ram_constraints`, `source_schema_version=6`, `third_copy_schema_version=7`, `legacy_tables_preserved=14`, `constraint_scenarios_passed=10`, `on_disk_sqlite_writes=false`, `production_migrated=false`, `active_pointer_modified=false`; candidate and SQL hashes matched. Independent PowerShell wrapper confirmed `M3.1 FINAL V7 READ-ONLY AUDIT : PASS` and **8/8 protected files unchanged**.

The ten RAM-scoped scenarios verified the actual candidate's fictional-calendar time modes and precision, revision/event/universe scoping, cross-Universe rejections, partial-order cycle guards and append-only rules. The tool read the v7 third-copy source via read-only SQLite and performed writes **only on an ephemeral `:memory:` clone**; this is not a production-app launch, runtime IPC E2E, or production v7 migration.

**Conservative acceptance boundary:** third-copy temporal-schema behavior and operator backup/rollback/read-only evidence are **PASS**. M3.1 is **not yet COMPLETE + MERGED + NORMALIZED**. Before considering controlled merge, qualify this evidence revision's *own exact HEAD CI*, compare PR scope/source against freshly fetched main, and explicitly resolve the roadmap's separate **controlled-launch/post-v7** gate. Normal startup is still capped at v6; no automatic registration of migration 007, no production v7 activation or M3.2 authorization.

## Unique Tauri isolated app identity preparation — actual Windows operator PASS

**Exact source HEAD:** `a6901c34f1a00f7c5e1e785882279e7f4e5a829d`, `pull_request` CI **#38153579902 completed/success 21/21 steps** (five new preparation fixture cases PASS, 100 Rust tests PASS). On target Windows, the six `m3_1_*` Python/SQL Git blobs and exact candidate SQL SHA-256 **`d66c26349e0bbfe0a9b9d610516c6ebe8d241d01f9506d0613f4152d25cd1212`** matched. Process preflight PASS (Fabulaxiom/Tauri/Ollama closed), and before/after exact hashes of **eight protected operator artifacts** all MATCH (restored production v6, v6 backup, preserved v6 restore and manifest, third candidate v7 and manifest, fourth rolled-back v6 and manifest). No historic M2.5 store was repurposed.

1. Final `--dry-run` returned `status=READY`, `mode=isolated_v7_launch_dry_run`, `isolated_identity_created=false`, `tauri_launched=false`, `production_migrated=false`, `third_candidate_sha256=566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402`.
2. Explicit separate `--prepare` returned **PASS**, `mode=isolated_v7_launch_prepared_not_launched`. New dedicated identity **`com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd`**, first such identity found (preflight count 0). Isolated database copy located only under `%LOCALAPPDATA%/com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd/database/fabulaxiom.sqlite3`, schema **v7**, byte SHA-256 **`566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402`** (same as protected third-copy source).
3. Exact isolated overlay `tauri.m31.isolated.conf.json` SHA-256 **`e377ae9ba9a0430928fec79700c31a74b6035a6f086e75bff19055766c118edc`**; preparation `preparation-manifest.json` SHA-256 **`9b718667487ed5776d141358d47e9f6dbb247a93fdc4c66a68baa42780d36da9`**. Independent PowerShell content checks verified overlay identifier, `bundle.active=false`, identical copy hash, manifest identity, expected `normal_v6_runtime_refuses_v7`, no production migration or pointer modification.
4. **`TAURI LAUNCHED: NO`**; `PRODUCTION SQLITE SCHEMA: V6`; eight protected source/custody SHA-256 values remain unchanged.

**Interpretation:** the isolated app identity and v7 bytes are prepared and independently hashed; the target-Windows actual launch, process identity checks, window behavior and post-launch custody audit are **NOT DONE**. The current normal Rust opener deliberately rejects SQLite v7 with `ExplicitMigrationRequired(7)`, so no claim of a positive v7-enabled desktop launch is appropriate. Before a graphical run, separately design and CI-qualify a preview/launch that opens v7 **read-only** under this exact identity and blocks all regular M2 write commands, then approve a bounded operator session with explicit shutdown and post-session SHA checks. The existing production `com.fabulaxiom.desktop` v6 identity and operator backup/third/fourth assets must remain untouched. Never infer Tauri process isolation merely from the overlay's presence; verify actual runtime identity and data path on launch. Official path semantics: https://docs.rs/tauri/latest/tauri/path/struct.PathResolver.html and config overlay: https://v2.tauri.app/develop/configuration-files/ .

## Actual Windows isolated v7 read-only Tauri graphical acceptance (2026-10-11)

**Qualified historical operator source:** PR #33 head `4d520e1825ecd08d20484b0e72d60ffe6ea09e4c`, exact-head CI #38160997846 completed/success. This section records operator-reported target-Windows terminal and visual observations, not a GitHub-hosted graphical test. New elevated-token preparer guard in this PR requires **its own** exact-head CI.

- Original unique identity `com.fabulaxiom.m31launchdb8d3278504c448084478a70ccb71cbd` reused, never another app identity. No production v7 migration and no automatic registration of SQL 007.
- The first isolated GUI attempt passed Vite and Rust compilation but failed at WebView2 initialization with `HRESULT(0x8000FFFF)` (exit code 101). Elevated-read-only NTFS forensics showed isolated root owner `BUILTIN\Administrateurs`, inheritance protected, and ACEs limited to OWNER RIGHTS / SYSTEM / Administrators, denying access from the real medium-integrity user. The root was created by Python `mkdir(mode=0o700)` under an elevated token; this was an access-control problem, not evidence of corrupt SQLite.
- Original root + seven descendant ACLs saved non-destructively with `icacls /save /T` in separate `Fabulaxiom-M31-ACL-Evidence-4d520e18` evidence folder. Operator added an explicitly scoped inheritable `Modify` ACE only for the current Windows user SID on the isolated root, leaving original owner, protected inheritance, old datasets and backups intact. A new standard-token Windows PowerShell 5.1 shell passed medium-integrity, root and descendant ACL read, 11/11 SHA-256 custody and M1.5 pointer unchanged.
- **Actual second GUI launch PASS:** fresh medium-integrity non-admin operator, Tauri `dev --features m31-isolated-preview --config` with preserved overlay and both explicit environment acknowledgments. Vite 8.0.16 ready, Rust debug compile completed (nonfatal unused-code warnings), executable started, operator saw **Fabulaxiom — v7 isolée** and the exact isolated identity, `Schéma v7 vérifié`, SQLite **7**, integrity **PASS**, foreign keys **PASS**, three empty STRICT time tables **3/3**, no write IPC registered, production migration **non**. This is actual UI and read-only IPC response, not merely a Vite-page observation. The session exited with code **0**.
- Separate new `operator-launch-baseline-attempt2-4d520e18.json` SHA-256 **`5f7b8c3d053c428d79eb36cf54cc658c75fdfa9fae6f99df1d5457e7825cfee5`** and `operator-launch-transcript-attempt2-4d520e18.txt` preserved, alongside original attempt-1 baseline/transcript. A live process observer STOPPED because it demanded exactly one `fabulaxiom.exe`; the observation did **not** resolve live executable path or PID. A separate subsequent post-session query found **zero** `fabulaxiom.exe` processes.
- **Actual post-close independent operator audit `M3.1 ATTEMPT-2 POST-CLOSE: PASS`:** Fabulaxiom/Tauri processes stopped, Vite/Ollama ports closed; both baseline protocols, source/identity, 11 names/paths/digests matched; **11/11** protected files (production restored v6, pre-v7 safety backup/restore/manifest, third v7/manifest, fourth rolled-back v6/manifest, isolated v7/config/manifest) unchanged; no unexpected SQLite `-wal`, `-shm`, `-journal`; identical M1.5 active restored v6 marker/path and SHA; detached source HEAD correct and clean. **WebView2 `EBWebView` cache directory was present** under the isolated identity.
- Anchor digests: restored production v6 `b904731afac0b6b6135ba6d6a8a8dee3548c50daca1a5ee3a7788db85cee16ff`; isolated candidate v7 `566db86d415b449de3f9f53145f6b830d6942ef4067c20df852ec3d722f54402`; candidate SQL Git-LF `d66c26349e0bbfe0a9b9d610516c6ebe8d241d01f9506d0613f4152d25cd1212` (local checkout differed **only** by CRLF).

**Boundary:** Controlled isolated read-only GUI/IPC plus post-close custody **accepted for qualified operator source**. No evidence of normal production v7 startup/activation is claimed or authorized: normal Rust still caps automatic migration at 6. The elevated-Windows-operator staging guard is a separate prevention enhancement; before merging this PR, its exact-head CI, updated scope and the roadmap's remaining acceptance language require review. M3.1 **not yet COMPLETE + MERGED + NORMALIZED**; M3.2 blocked.
