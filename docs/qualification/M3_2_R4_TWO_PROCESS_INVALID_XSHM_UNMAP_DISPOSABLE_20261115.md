## Réconciliation du 15 novembre 2026 après #371

PR #371 P3ag MERGED, main `7abf9bae9179628fcc7bf368cc6a74ab86f7a808`, CI Windows source #43723270617 SUCCESS au HEAD exact `a0d059ba44c920740f38765149e43682a788107b`. Postmain #43724388071 PENDING_UNQUALIFIED au checkpoint. Le candidat R4 #372 garde **uniquement** le refus `xShmUnmap(-1/2)` dans deux processus Windows jetables, sans exécuter d'unmap valide sur SQLite vivant. Ancien HEAD R4 `6bca6565316206a8c56930a171e234365bfa7c9a` et CI #43724262869 **NON TRANSFÉRABLES** à ce nouveau HEAD. Source Windows COMPLETE au HEAD réconcilié et postmain indépendante parent terminal SUCCESS requises avant toute fusion. Aucune permission writer ou G3, main/WAL/SHM et ABA NON PROUVÉS. Checklist 9/104, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45%), glib #160 OPEN.

# R4 — refus de deux xShmUnmap invalides et mémoire SHM tenue, 15 novembre 2026

## Parent
`main=eedf2f571ea3e4e07da4fd992dae515515c016a8` après #370 MERGED ; CI source #43719583953 SUCCESS HEAD exact `0e17d38fe30fab1329830ee818dd613b28805b42` et postmain #43722727745 SUCCESS au SHA exact. PR #371 produit P3ag en cours, travail R4 indépendant. Avant toute fusion, re-fetch current main, requalification du diff et CI complète au SHA candidat, reviews/threads, Protect main ACTIVE strict `bypass_actors=[]`, squash `expected_head_sha`, postmain indépendante et #38 append-only.

## Preuve candidate
La fixture Rust `#[cfg(all(test,windows))]` déjà qualifiée pour deux processus OS, WAL NORMAL sur nouveaux fichiers %TEMP% et SQLite `SQLITE_FCNTL_FILE_POINTER` est étendue. Chaque processus appelle effectivement le pointeur natif `xShmUnmap` avec les valeurs invalides -1 et 2 ; vérifie SQLITE_IOERR_SHMMAP, aucune augmentation du compteur des unmaps réussies, hausse du compteur de refus, puis nouvel accès à la région SHM 1 avec pointeur strictement inchangé. Les identités natives main/SHM sont encore vérifiées. Le vrai SQLite ferme lui-même normalement la connexion ; le test ne détache jamais prématurément une région tenue.

## Interdictions et limites
Ceci ne prouve **ni** un cycle complet de xShmUnmap valide sous partage/processus, **ni** une frontière de capture atomique main/WAL/SHM, **ni** l'exclusion d'ABA invisible, **ni** les droits writer. M32-017/019/020 restent [ ] ; R1–R9 writer NOT_PROVEN, P4 STOP, G2B/C/G3 STOP, glib #160 OPEN. Checklist 9/104 closes, 95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %), PRODUCT_FIRST_PARALLEL_SAFETY. Pas de code runtime, profil opérateur, originaux v6/v7, backup, Greenfield, IPC, 007, Windows Hello ou recovery.
