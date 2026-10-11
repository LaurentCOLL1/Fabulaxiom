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

1. **Operator failed-migration rollback on another disposable copy** with proof of atomic refusal/no partial v7 schema, while production, backup, restore and source pointer remain unchanged. Source fixture failures alone are not substitute operator evidence.
2. Independent audit of historical content and critical triggers/source links against the *actual* v7 rehearsal as needed, including the absence of unforeseen chronology mutation; retain all evidence.
3. Evidence commit's **own exact-head terminal `pull_request` CI PASS** (prior #38122561283 qualifies original code HEAD only); fresh GitHub comparison and applicable review/merge authorization.
4. Only then evaluate the separately governed PR merge and post-merge normalization. **Do not automatically register 007 in normal startup, do not upgrade production from v6, and do not authorize M3.2+.**

The real Windows third-copy PASS is **not** a production migration acceptance. SQLite reference: https://www.sqlite.org/backup.html ; https://www.sqlite.org/pragma.html .
