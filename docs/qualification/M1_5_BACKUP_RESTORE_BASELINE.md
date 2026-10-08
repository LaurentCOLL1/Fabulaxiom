# M1.5 — Safe SQLite Backup and Restore Baseline: Windows Qualification

## Gate

**COMPLETE + MERGED + NORMALIZED**

This record preserves the qualified M1.5 implementation and Windows backup/restore evidence. The final evidence commit received terminal CI, PR #15 merged and the project authority is being normalized in a separately qualified PR. M2 code still requires an approved detailed M2 scope.

## Source and Git authority

Repository: private `LaurentCOLL1/Fabulaxiom`.

Implementation PR: **#15 — feat: implement M1.5 safe SQLite backup and restore baseline**.

Branch: `feat/m1-5-backup-restore-baseline-20261008`.

Base live `main`: `2c942c5b58f316a5f02f69abfcf3883fb9d5929e`.

Qualified implementation HEAD: `7f968075f632843144c9833f61cc51910b538530`.

Windows local repository: `M:\Fabulaxiom`.

Operator reported:

- worktree clean before and after qualification;
- main/feature remote SHAs exactly matched;
- tracking feature branch created from origin;
- dependency locks unchanged;
- Fabulaxiom and Ollama closed before the deterministic checks.

## Delivered baseline

- application-owned snapshot backup through SQLite `VACUUM INTO`;
- unique non-overwriting filenames in the app-local `backups` directory;
- schema owner, migration lineage, integrity and foreign-key validation;
- backup listing and deterministic application/Tauri error payloads;
- restore of an app-owned backup to a *new* database file;
- independent validation prior to activation;
- activation marker switch without overwriting the previous active DB;
- no removal of historical operator backup files;
- Rust services / thin Tauri commands / React backup-and-restore controls;
- explicit confirmation before activating the restored database;
- no new dependencies and no Ollama requirement.

Previously retained historical backup files, including pre-M1.2 and pre-M1.4 backups, must remain untouched.

## Deterministic local Windows qualification

Exact source HEAD:

`7f968075f632843144c9833f61cc51910b538530` — **PASS**.

`npm ci`: **PASS**; npm audit reported 0 vulnerabilities.

`npm run test:ci`: **PASS**, 5 files, **13/13 tests**.

`npm run build`: **PASS**, TypeScript and Vite production build.

`cargo test --manifest-path src-tauri/Cargo.toml --all-targets --locked`: **PASS**, **37/37 tests**.

`cargo check --manifest-path src-tauri/Cargo.toml --locked`: **PASS**.

`git diff --exit-code -- package-lock.json src-tauri/Cargo.lock`: **PASS**.

Final worktree: **CLEAN**.

Rust reported three **nonfatal** warnings in `src-tauri/src/backup.rs`:

- unused import `File`;
- unused payload fields of `BackupError::Io`;
- unused payload fields of `BackupError::Sqlite`.

No test/build failures. These warnings do not change the observed backup/restore behavior and were not modified after operator qualification.

Pre-evidence exact-head GitHub Actions:

- workflow `Fabulaxiom CI`;
- run `37718677686`;
- `completed/success`;
- frontend 13/13, Rust 37/37 PASS, build/check and immutable lockfiles PASS.

This prior run is historical after an evidence commit; it cannot authorize merging a new HEAD.

## Windows interactive backup qualification

With Ollama stopped, the operator launched Fabulaxiom via `npm run tauri dev`.

Diagnostics:

- `Vérifier la base locale`: **SQLite schema v3 PASS**;
- `Tester le pont Rust`: **PASS**;
- `Vérifier Ollama local`: **INDISPONIBLE**, expected.

App command: `Créer une sauvegarde vérifiée`.

Observed UI:

**PASS — Sauvegarde validée (schéma v3)**.

Exact backup path:

`C:\Users\lauco\AppData\Local\com.fabulaxiom.desktop\backups\fabulaxiom-backup-00000000000001791428029335746400-0000025660-0000000000.sqlite3`

Reported retained counters:

- 1 universe;
- 1 novel;
- 1 scene;
- 3 scene text revisions;
- 1 current revision head.

## Windows interactive restore qualification

The operator selected the newly created application backup, confirmed its restoration and allowed the UI to reload.

Operator-reported result: **PASS**.

After restore/reload:

- the universe and novel remained present;
- the scene remained present;
- all three historical revisions remained accessible;
- the expected current revision remained selected;
- hierarchy remained intact;
- Tauri run exited normally.

Application's restore design verifies the selected app-owned backup, creates an independent SQLite file, and commits an activation marker only after validation. Tests cover the backup/restore preservation contract.

**Evidence precision:** The operator did not paste the restored active database's filename, the prior database filename or an independent post-restore `PRAGMA integrity_check` output. Consequently this record asserts the UI-observed restoration and successful application verification, not independently measured post-restore file paths or a new post-restore external integrity scan.

No database file or backup was intentionally deleted.

## Existing safety test coverage

The Rust test suite passed cases covering:

- consistent snapshot and no mutation of live database;
- non-overwriting unique backup filenames;
- restore to a new database preserving original data, revision history, provenance and current heads;
- path traversal rejection;
- corrupt backup rejection without activation;
- failed activation preserving previous active database;
- deterministic Tauri error serialization and explicit confirmation.

These are controlled automated tests; the operator-qualified Windows flow is additional live evidence.

## Terminal exact-head CI and merge

Qualification evidence commit:

`152b40e616f40799abc61f9ce8db142e3b19340b`

Terminal `Fabulaxiom CI` run:

`37720676744` — **completed/success**

- frontend tests: 13/13 PASS;
- Rust tests: 37/37 PASS;
- frontend production build: PASS;
- `cargo check --locked`: PASS;
- dependency lockfiles unchanged.

The previous implementation SHA CI `37718677686` is historical only and was **not** reused to authorize merging the documentation SHA.

PR #15 merged with expected-head protection.

Implementation merge:

`282b325fb6c588a70df08a5128415c8fa0a0f72e`

Post-merge live `main` re-fetched and confirmed at this merge commit.

## Governance conclusion

M1.5 implementation, Windows operator qualification, exact-head evidence requalification and implementation merge are complete. This document is part of the separate M1.5 post-merge normalization that closes M1.

M2 is only authorized for roadmap/architecture planning, not implementation, until a detailed M2 authority is accepted.

The historic M1.2 and M1.4 operator SQLite backups and all app-created backups must remain preserved.
