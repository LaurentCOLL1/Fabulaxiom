# M3.2 R4 — three file no-delete-share guard during normal SQLite WAL (Windows disposable)

## Premier refus sécurisé de CI et mise à jour ciblée de l'inventaire — 8 novembre 2026

HEAD source initial `f2c73798019933b9f69715ce449719c1c95b4493`, Windows #42469900496 **FAILED (fail-closed)** au contrôle `M3.2 whole-tree Rust SQLite source-only inventory and 21 drift refusals` : ajout réel d'**un** `Connection::open_with_flags_and_vfs` avec `SQLITE_OPEN_READ_WRITE` dans le module R4 Windows `#[cfg(test)]` déjà inventorisé. Le déclenchement a empêché l'intégration silencieuse d'une nouvelle ouverture SQLite. Après revue de la portée strictement jetable, `tools/m32_rust_sqlite_open_inventory.py` reconnaît précisément le comptage du **seul** fichier R4 **(17,0,0,0,0,17,0) → (18,0,0,0,0,18,0)** ; les cinq assertions explicites `tools/test_m32_rust_sqlite_open_inventory.py` sont alignées et vérifient aussi le nom exact du nouveau test. **Aucun pattern de détection, refus de drift, contrôle de production ou test négatif n'a été supprimé ou assoupli.** Tous les autres chemins SQLite gardent leurs comptages exacts. Les CI suivantes doivent être qualifiées au SHA final ; ne pas déduire d'admission writer de ce ré-audit.


8 novembre 2026 — **CANDIDAT NON QUALIFIÉ**. Parent protégé `main=7c05704c4da4ac50d5ee34829fb80751a4cc6b83` (#318), parent postmain Windows #42469381416 à qualifier. Stratégie PRODUCT_FIRST_PARALLEL_SAFETY inchangée ; prévenir AVANT changement.

## Pourquoi cette expérience

La preuve R4 du 7 novembre avait montré qu'un HANDLE sur WAL avec `FILE_SHARE_READ|FILE_SHARE_WRITE` sans `FILE_SHARE_DELETE` interdisait son renommage et restait compatible avec SQLite WAL NORMAL sur fichiers TEMP neufs. **Ce test ne prouvait rien sur le garde simultané des trois noms.** Microsoft documente que FILE_SHARE_DELETE autorise l'accès DELETE nécessaire au renommage, donc que son omission maintient une protection **pendant la vie de chaque HANDLE**. SQLite documente que NORMAL WAL recourt aux méthodes `xShmMap/xShmLock/xShmBarrier/xShmUnmap` plutôt qu'au raccourci EXCLUSIVE.

Références externes : https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew et https://www.sqlite.org/wal.html .

## Test limité

`src-tauri/src/m32_r4_registered_owned_shm_vfs_disposable_tests.rs`, nouveau `#[test]` :

1. `Scratch::fresh()` crée des fichiers `invented.sqlite3` et `invented.sqlite3-shm` sous un dossier de TEMP strictement neuf ; le VFS enregistré pour les tests crée le WAL `invented.sqlite3-wal`.
2. Trois HANDLEs distincts sont ouverts **successivement** avec partage READ|WRITE et refus de partage DELETE. Trois FileId128 natifs sont comparés aux masters VFS test-only ; des tentatives de renommage de chaque nom doivent échouer, et une réouverture READ|WRITE doit conserver l'identité native.
3. La connexion SQLite **NORMAL** passe en journal_mode=WAL, exécute un INSERT/SELECT fictif, puis vérifie les callbacks SHM et l'identité WAL prétenue par VFS, et tente de renommer à nouveau les trois fichiers pendant que SQLite les utilise.
4. Ferme ensuite explicitement SQLite, le VFS enregistré et les trois guards, avant le cleanup du seul dossier de TEMP créé par le test.

Les garanties du test restent **strictement bornées** : ces handles sont pris **l'un après l'autre** (et pas atomiquement) ; le test ne prouve pas l'absence d'ABA **avant** capture, ni l'identité de tous les handles privés internes de SQLite, ni la custody atomique des trois fichiers, ni un comportement multi-processus en production, ni la reprise après crash. La présence d'un INSERT/SELECT dans une base jetable de CI **n'est PAS** une activation du writer réel.

## Qualification attendue, refus strict jusqu'au CI source exact

Un nouveau Rust attendu, **332 Rust**, 7 Greenfield, 69 inventaire SQLite, 183 continuité, 408 Vitest, Chromium 88/88 normal + 88/88 CSP stricte, 25 blobs source fictifs. Nombres **ATTENDUS/NON PASS** avant CI terminale du HEAD exact. Parent postmain SUCCESS exact SHA, diff/reviews/threads, Protect main ACTIVE strict bypass=[], squash `expected_head_sha`, postmain indépendant, issue #38 append-only.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimation), writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, custody atomique main/WAL/SHM et absence d'ABA non observée `NOT_PROVEN`, glib #160 `OPEN_NOT_REMEDIATED`. Aucun profil Greenfield existant, base opérateur v6/v7, backup/journal, IPC writer, migration 007 runtime, Hello natif, marqueur/recovery.
