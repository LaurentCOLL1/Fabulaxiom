## 15 novembre 2026 — requalification après fusion de #368

PR #368 P3ae fusionnée sous Protect main : `main=b52db55a3b05129b80c3f33b53a7d8b0e3e8dcc6`, CI Windows source [#43697691761](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43697691761) SUCCESS au HEAD exact `8304b433148a2a222fa11f184083d435bef7b179`. Postmain [#43699940967](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43699940967) NON QUALIFIÉE tant que son état n'est pas terminal SUCCESS. La branche R4 #369 a été réconciliée depuis `f55e3838b23ebcb1ccefbac7e2a97b0c68cfbded`, en conservant aussi les preuves produit P3ae, les 104 points de la checklist (9 clos/95 ouverts) et les STOP. Toute CI sur les anciennes têtes de #369 est NON TRANSFÉRABLE : une CI Windows complète sur le HEAD après cette modification documentaire est nécessaire, puis revues/threads, Protect main strict, expected_head_sha et postmain indépendant. R4 main/WAL/SHM, races ABA, writer et G3 restent NOT_PROVEN/STOP.

# R4 — xShmBarrier et refus xShmLock en deux processus Windows (15/11/2026)

## Source et portée

Parent protégé `main=85c246ce723ca9866935e1226d8e6fb0c0bd9a59`, #367 P3ad MERGED. #367 source Windows CI #43668424751 SUCCESS HEAD exact `c697cc0191987f30d5fb83249ddd50434b791147` et postmain #43695902106 COMPLETED/SUCCESS au SHA exact parent. `Protect main` ACTIVE strict `bypass=[]`. La PR R4 doit être qualifiée indépendamment au HEAD exact, comme #368 produit parallèle.

Modification uniquement dans le module `src-tauri/src/m32_r4_registered_owned_shm_vfs_disposable_tests.rs`, activé depuis `src-tauri/src/lib.rs` sous `#[cfg(all(test, windows))]`. Aucun VFS de production ni connexion opérateur.

Extension de `r4_assert_owned_multiprocess_region_one` : à partir de l'objet `sqlite3_file` que SQLite possède réellement dans **chacun des deux processus Windows**, après xShmMap régions 0/1 :
- Obtient `xShmBarrier` depuis `pMethods` et l'appelle deux fois. Il s'agit d'une barrière SeqCst locale, **pas** d'une preuve de synchronisation interprocessus universelle.
- Obtient `xShmLock` de ce même objet, vérifie le refus `SQLITE_IOERR_SHMLOCK` pour un verrou partagé de largeur 2 et un index 8 hors bornes.
- Confirme que ces refus n'incrémentent pas le compteur de verrous natifs et incrémentent le compteur de refus ; contrôle les identités FileId128 déjà tenues main/SHM après les appels.
- Préserve les handshakes A `BEGIN IMMEDIATE` / B `BUSY` puis admission après COMMIT, somme fictive attendue 24 et fichiers TEMP `CREATE_NEW`.

## Critères d'évidence (candidat)

Le Rust Windows test-only doit passer dans `cargo test --locked` au HEAD exact de la future PR ; revues/threads, Protect main strict, `expected_head_sha` et postmain indépendante obligatoires. Sans statut terminal, aucune promotion. M32-017/019/020 [ ] : couverture limitée des callbacks, **aucune** preuve de capture atomique main/WAL/SHM, de vie entière WAL-index ou d'absence d'ABA invisible.

## Sécurité

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 %) ; checklist 104 = 9 closes/95 ouvertes. `PRODUCT_FIRST_PARALLEL_SAFETY` maintenue ; writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; R2 STOP, R3 partiel ; D3c conception, D3b-4/5 et D3b-5 STOP. Aucune lecture ou modification v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello ou recovery. Vulnérabilité `glib 0.18.5` issue #160 OPEN_NOT_REMEDIATED, lockfiles inchangés.
