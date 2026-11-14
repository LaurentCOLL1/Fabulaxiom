# R4 — deux processus Windows : région SHM 1 tenue et inspectée via SQLite

**15 novembre 2026 — CANDIDAT NON QUALIFIÉ, SANS WRITER.** Source parent `main=c1435a612c45489f1f6e07b557662fac1b6b5245` (#364 MERGED), source [#43620011103](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43620011103) SUCCESS exact HEAD, postmain indépendante [#43621231640](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43621231640) SUCCESS SHA exact. La CI de la présente modification reste à qualifier à son propre HEAD.

## Modification source bornée

Dans `src-tauri/src/m32_r4_registered_owned_shm_vfs_disposable_tests.rs`, VFS explicitement NON DÉFAUT et exclusivement `#[cfg(all(test,windows))]`, les deux processus OS déjà existants (`r4_multiprocess_wal_child_helper`, `r4_two_windows_processes_serialize_wal_writes_on_fresh_owned_shm`) partagent seulement le dossier neuf %TEMP% créé par le parent. Un helper commun exige :
- `SQLITE_FCNTL_FILE_POINTER` sur la connexion SQLite pour récupérer le **vrai** `sqlite3_file` ;
- callbacks `xShmMap` région 0 puis région 1, taille exacte 32768 octets, extension `0` et pointeurs non nuls avec offset de 32768 ; ceci **n'écrit pas** dans la mémoire partagée ;
- FileId128 natifs du HANDLE SHM et du HANDLE main **tenus par chaque processus**, toujours conformes à leurs IDs attendus ;
- exécution dans le parent avant/et après le handshake multi-processus, dans l'enfant après constat `SQLITE_BUSY` ou `SQLITE_LOCKED` puis avant le signal de disponibilité. Le protocole existant termine au total fictif `11 + 13 = 24` avec délais bornés.

Aucun nouveau `Connection::open*`, aucun nouveau champ de VFS de production, aucune donnée opérateur, API Tauri, IPC writer, migration 007 ou recovery. Les gardes de source SQLite existants doivent demeurer stricts.

## Portée & limites de la preuve

**Amélioration attendue** : chaque processus confirme qu'il peut mapper la deuxième page du SHM détenu sur le `sqlite3_file` effectivement ouvert et que ses FileId128 natifs main/SHM sont stables pendant ce témoin. Ceci ne prouve pas que les vues des deux processus partagent un invariant anti-ABA atomique, ni que SQLite utilise exclusivement ces handles pour la totalité du WAL-index. La région SHM 1 testée n'est pas un modèle complet des régions supplémentaires ou du cycle de vie `xShmUnmap`.

Aucune capture atomique des objets `main/-wal/-shm`, pas de prévention démontrée de remplacement entre contrôle et `xOpen`, pas de résistance à un écrivain hostile même SID et pas de confinement des alias/reparse points. **M32-017/019/020 demeurent [ ]** et writer/R1–R9 `NOT_PROVEN`. Les autres R2–R9, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, P4 STOP et glib #160 OPEN_NOT_REMEDIATED sont inchangés.

## Qualification

CI Windows exacte HEAD, logs du test R4 à deux processus, full Rust + source inventory, reviews/threads, Protect main ACTIVE strict bypass=[], guarded squash `expected_head_sha`, postmain indépendante et issue #38 append-only. Cette expérience cible le blocage M32-017/019 **sans** prétendre les clôturer ; M3.2 reste IN_PROGRESS_NOT_ACCEPTED (~45%), checklist 9/104 closes/95 ouvertes. P3ac produit est développé en parallèle, sans couplage avec ce VFS.

Documentation SQLite : [WAL](https://www.sqlite.org/wal.html) ; [VFS sqlite3_file](https://www.sqlite.org/c3ref/file.html) ; [file-object WAL](https://www.sqlite.org/c3ref/database_file_object.html).
