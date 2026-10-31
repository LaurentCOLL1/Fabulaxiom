# M3.2 — R4 / D3a live SHM FileId128 (Windows fixture only)

**30 octobre 2026 — CANDIDAT NON QUALIFIÉ.** Parent protected main `fd6b7ccfd45d877ea34c5c02668660b3a17ffc27` from PR #243. Source PR #243 [Windows CI #41119276800](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41119276800) completed/SUCCESS at exact PR head `9630eb43f4d3934b827109291c8e6c93f0036fe9`: 268 Rust / 7 Greenfield / 55 SQLite inventory / 165 continuity. Independent [postmain push #41123096907](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41123096907) **IN_PROGRESS at drafting; re-fetch terminal SHA separately.**

## New narrowly bounded CI witness

`m32_r4_d3a_shm_fileid_stable_during_live_wrapped_wal_disposable` in `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`, reachable **ONLY** with `cfg(all(test,windows))` via existing test-only VFS Rust module. On a brand-new invented `%TEMP%` SQLite main:

- The existing D3a fixture delegates normal Win32 SQLite xOpen, checks the main FileId128 after delegated xOpen, checks WAL's delegated opened handle identity, and wraps all `xShmMap`, `xShmLock`, `xShmBarrier`, `xShmUnmap` and close.
- While the disposable WAL-mode SQL connection is alive, separately open the invented `-wal` and `-shm` with FILE_SHARE_READ|WRITE, hold FileId128 from each actual Win32 handle, ensure all three identities are distinct, issue a second **invented fixture SQL** insert and verify both held sidecar identities and freshly observed names continue matching.
- Explicitly release the test-only additional sidecar handles *before* the existing SQLite connection's close/checkpoint lifecycle; assert successful D3a SHM unmap and main/WAL xClose callbacks.

**What this does NOT prove:** SHM mapped handle ownership (xShmMap is still delegated to stock Win32 and may open its own file); atomic custody of main/WAL/SHM, protection against pathname ABA, a production preopened R3 xShm* VFS, cross-process authenticated lifecycle, repair, checkpoint durability, crash recovery, permission to use operator v6/v7 sidecars/backups or the existing Greenfield profile, native Hello, migration 007, durable marker, actual writer IPC, or M3.2 admission.

**Expected, NOT CI PASS until exact-head source CI and logs:** 269 Rust / 7 Greenfield / 56 inventory / 166 continuity. No changes to the runtime entrypoint. Only new fixtures, source guard counts, protected branch and continuity.

## Mandatory protected qualification

Exact PR HEAD, Windows status `completed/SUCCESS` and logs, full diff/reviews/threads, `Protect main` #24895490 ACTIVE strict required `Windows frontend and Rust checks`, bypass=[], protected squash using `expected_head_sha` only if admissible, independent postmain exact SHA, issue #38 append-only. Parallel code/document review allowed; never treat draft candidate as accepted.

**STOP:** M3.2 IN_PROGRESS_NOT_ACCEPTED; writer/R1–R9 production NOT_PROVEN; G2B NOT_ACCEPTED; G2C NOT_AUTHORIZED; real G3 STOP_UNAVAILABLE; historical PENDING_EXTERNAL_ATTESTATION(21/3/2); prospective NOT_STARTED; D3b-4/5 and D3b-5 STOP; D3c design-only.

**Next architecture:** prove a handle-bound `xShm*` path for preopened R3 main with WAL/SHM identity pinned throughout transitions, on *new fixtures only*; until then fail closed. SQLite [WAL](https://www.sqlite.org/wal.html) and [WAL-index](https://sqlite.org/walformat.html) are normative context, not admission.

## Correctif de périmètre historique, CI initiale refusée

[CI Windows #41123585787](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41123585787) FAILED à `aba507618e15789f7df148a07f98343242d189b9`, dans cinq tests du contrat de continuité : le nouveau test avait été ajouté **à l'intérieur** de la tranche historique D2/D3ab, dont les 26 tests d'origine sont figés. Correctif sans changement de la politique ni des tests historiques : déplacer le test R4/D3a dans un **nouveau module autonome placé après la section historique**. Le témoin demeure `cfg(all(test, windows))`, les mêmes VFS de test et fichiers fictifs, sans aucune activation en production ; il construit sa propre main SQLite neuve au lieu d'utiliser `fresh_main()` du module historique. Les 26 tests historiques restent strictement 26 ; le total Rust attendu reste 269. **Nouvelle CI exact-head obligatoire avant toute fusion.**

## Seconde tentative CI : assertion d'inventaire du nouveau module

[CI Windows #41123849481](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41123849481) **completed/FAILURE** au HEAD `c3c35904435f8d20864ce88fcc15d59e0eb64c86` : les contrats des 26 tests historiques passent, mais le nouveau `test_56` attendait encore `fresh_main()` alors que le module autonome utilise `let owned = DisposableRoot::new()` et `create_new(true)`. Correction limitée à ce garde source : exiger explicitement la création neuve indépendante et le VFS D3a ; **aucune modification du code Rust**, et aucun changement des comptes 269/7/56/166 attendus. Nécessite une nouvelle CI exact-head et la lecture de ses logs.

## Troisième tentative CI : frontière entre les deux R3 historiques et R4 autonome

[Windows CI #41124188198](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/41124188198) **completed/FAILURE** sur `e5eb002c584b15884898a762d664281842d67b13` : les 56 tests d'inventaire ont réussi ; le contrat historique `test_156` comptait tous les `#[test]` après le marqueur R3, y compris le nouveau module R4 situé après les deux tests historiques. Correction ciblée : vérifier que le marqueur de module R4 apparaît exactement **une fois**, puis délimiter la région R3 historique avant ce marqueur et y exiger toujours exactement **2** tests. Les 26 tests D2/D3ab et 5 témoins R4 P1 restent protégés par leurs contrats exacts. Aucun changement de code Rust ni d'opération opérateur ; une nouvelle CI exact-head reste obligatoire.
