# M3.2 R4 — normal WAL read refusal without xShm* (disposable candidate)

**30 October 2026 — UNQUALIFIED until exact-head Windows CI.** Base main `6166a256e479ef7cd3c1a6cacdaccaadb68cfb49` after PR #242 protected squash, exact PR #242 source [#41084067311](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41084067311) completed/SUCCESS 267 Rust / 7 Greenfield / 54 SQLite inventory / 164 continuity. [Independent postmain #41110676555](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41110676555) was IN_PROGRESS at drafting; independently re-check its terminal outcome.

## Bounded negative witness

New test `m32_r4_readonly_preopened_vfs_without_xshm_refuses_live_wal_disposable` only in `#[cfg(all(test, windows))]`. Creates an invented SQLite `%TEMP%` database and holds the standard SQLite Win32 writer on that **new test file only** while WAL and SHM exist. Attempts `NORMAL` locking read with the existing Fabulaxiom **test-only READ_ONLY** VFS using `sqlite3_io_methods.iVersion=1`, `xShmMap=None`, `xShmLock=None` and no custom WAL custody. Requires SQLite to refuse WAL reading (on open or first query) and verifies stock writer still reads unchanged invented content. No data outside test's unique new root is accessed.

SQLite's [WAL documentation](https://www.sqlite.org/wal.html) says a VFS without shared-memory methods cannot normally read a WAL database in NORMAL mode. The EXCLUSIVE-before-first-access exception **does not authorize bypassing R4** and is not used here.

**Expected, NOT PASS until CI:** 268 Rust / 7 Greenfield / 55 SQLite inventory / 165 continuity.

This negative result does **not** prove positive xShm* forwarding, atomic WAL/SHM FileId128 custody, multi-process correctness, checkpoint, crash recovery, real R1–R9, or writer admission. No production change, no operator v6/v7 or existing Greenfield profile, IPC, migration 007, Windows Hello native, persistent marker or recovery.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historical PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED. D3b-4/5 and D3b-5 STOP, D3c design only.

**Next:** exact HEAD Windows CI, diff/reviews/threads, active strict Protect main bypass=[], protected expected_head_sha squash if PASS, independent postmain and #38 append-only; then positive xShm* sidecar ownership on new fixtures, never promotion to production.

## CI source, tentative initiale refusée

[Windows CI #41111319310](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41111319310) completed/FAILURE au HEAD initial `b664240e3ebcb17f2ed1a5a2fd058ccb7f80079c` ; l'inventaire a correctement détecté le nouveau total **5** occurrences `Connection::open*` et **4** `SQLITE_OPEN_*` dans le module, alors que les attentes indiquaient 4/3 et que les contrats R3 conservaient 3/3. Cette défaillance n'est jamais qualifiée PASS. Le commit correctif met à jour tous les comptes source-only à `(5,0,0,0,0,4,0)`, sans nouveau site d'ouverture ni changement de comportement runtime. **CI du HEAD corrigé à vérifier séparément avant tout merge.**

## Seconde tentative CI : garde de portée R3 vs R4

[Windows CI #41118520549](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41118520549) a refusé le HEAD `9b8b1c2ad614135113fe91a1138560a6116cac3a` dans les 55 contrôles d'inventaire source : **cinq protections R3 historiques** interdisent `PRAGMA journal_mode=WAL` partout dans ce module désormais partagé avec le nouveau témoin R4. Correction : ces cinq tests continuent de refuser tout `PRAGMA journal_mode=WAL` dans **l'intégralité de leur section R3 antérieure au nouveau marqueur exact**, et interdisent toujours IPC, migration ou ouverture production dans **tout le fichier**. L'unique section R4 distincte reste bornée à `cfg(all(test,windows))`, fichier jetable, stock-VFS writer fictif, lecture custom READ_ONLY refusée. Aucune suppression du contrôle R3 ; pas de qualification sans nouvelle CI exact-head. Historique d'échecs conservé.

## Troisième tentative CI : continuité historique du prompt court

[CI Windows #41118844657](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41118844657) **completed/FAILURE** sur `5e64a90927cca2c80eb440bcbea0f0efe80a47db` : les 55 contrôles inventaire ont franchi le gate, mais `test_164_r4_stock_win32_wal_shm_candidate_never_admits_writer` a refusé l'absence de référence littérale à la qualification antérieure `M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md` dans le prompt court. Le correctif rétablit ce lien et consigne le résultat postmain #242 SUCCESS. Aucune modification Rust, ni promotion R4. La CI du nouveau HEAD doit être vérifiée séparément ; aucun ancien échec n'est un PASS.
