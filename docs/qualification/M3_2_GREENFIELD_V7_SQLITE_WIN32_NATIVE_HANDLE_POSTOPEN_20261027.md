# M3.2 — témoin natif SQLite Windows `xOpen` : identité du fichier, post-ouverture seulement

**CANDIDATE NON QUALIFIÉE — tests/fixtures Windows GitHub jetables seulement.** Base observée en direct le 27 octobre : [PR #194](https://github.com/LaurentCOLL1/Fabulaxiom/pull/194) **MERGED**, source exacte `de54c003421d09309f5bff8a31d110fb24d93678`, [CI source #40507105063](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40507105063) SUCCESS (151 Rust, 7 Greenfield, 32 gardes, 125 contrats), squash protégé `main=567638515444d621749507f9700a3e2a69c52c6b`, [postmain #40508416842](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40508416842) SUCCESS indépendante, [issue #38 terminale #6442750005](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6442750005). Cette CI **ne qualifie pas** la nouvelle candidate.

## Question précise et expériences

La PR #194 a réellement montré que des répertoires Windows **vides** pouvaient être renommés malgré des handles détenus avec partage sans DELETE ([échecs #40499869627 et #40501278786](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40501278786)). La révalidation ponctuelle des répertoires peut détecter un changement **déjà arrivé**, mais elle ignore un remplacement du fichier **après** le contrôle et **avant** `xOpen`. Aucune admission hostile n'était prouvée.

Ce laboratoire enrichit `src-tauri/src/world_time_file_migration_tests.rs`, exclusivement `#[cfg(test)]` et `#[cfg(windows)]`, sans modifier le runtime :

1. Appelle `sqlite3_file_control(db.handle(), "main", SQLITE_FCNTL_WIN32_GET_HANDLE, &HANDLE)` **après** `Connection::open_with_flags(..., SQLITE_OPEN_READ_WRITE)`. SQLite documente cet opcode Win32 pour obtenir son vrai handle VFS. Celui-ci est **emprunté** : ni fermeture, ni échange via `SQLITE_FCNTL_WIN32_SET_HANDLE` (opcode de débogage), ni changement de VFS.
2. Compare l'identité **volume + FileIndex 64 bits** lue avec `GetFileInformationByHandle` sur ce handle SQLite à celle du **handle de revendication `create_new(true)`**. Fixture positive : identité égale tant que le claim Windows est conservé, puis `SELECT 1` uniquement après comparaison.
3. Fixture **négative** : prévalidation réussie, libération volontaire du claim (pour reproduire un handoff insuffisant), renommage du fichier original *dans la même racine jetable*, nouvelle création sous le **même nom**, nouvelle vérification des répertoires toujours verte, puis `xOpen` qui suit le nom remplacé. La comparaison **post-`xOpen`** doit refuser l'identité étrangère avant tout SQL applicatif. L'original déplacé, le nouveau fichier et l'absence de marqueur d'activation sont vérifiés.

**Cibles, pas PASS anticipés** : 153 tests Rust (2 Windows), 7 tests Greenfield inchangés, 34 gardes textuels d'inventaire, 126 contrats de continuité. Occurrences textuelles revues pour le module : `(19,4,3,2,0,7,0)` ; exactement une ouverture RW supplémentaire, `#[cfg(windows)]` dans un module `#[cfg(test)]`. Ni `Cargo.lock`, ni workflow, ni SQL de migration, ni Tauri IPC changés.

## Portée et STOP

**Un refus après `xOpen` n'est pas une ouverture atomique ni une prévention du passage à un fichier substitué.** SQLite peut déjà avoir ouvert le mauvais fichier ou effectuer des opérations VFS avant le contrôle. La comparaison est ponctuelle : substitution ultérieure, fermeture/réouverture, identité réutilisée, verrouillage/journaux et sidecars, chemins de journaux, reparse/junction, racines supérieures, ACL et adversaire hostile ne sont pas couverts. La preuve négative **suppose délibérément la libération du claim** ; elle ne prouve aucun déplacement possible pendant une revendication conservée. ReFS requiert notamment l'examen séparé de `FILE_ID_INFO` 128 bits ; FileIndex 64 bits ne suffit pas à garantir son identité. Aucune future fonction de production ne devra considérer ce seul contrôle comme autorisation de faire du CRUD.

Aucun projet historique, SQLite v6/v7 opérateur, backup, sidecar actif, marqueur, ACL, journal ou writer IPC n'est consulté/modifié. Profil unique `com.fabulaxiom.greenfield.v1` inchangé ; aucun ouvreur/CRUD/UX v7 Tauri, aucune migration 007, aucune autorisation G2B/G2C/G3, aucune release et aucune attestation Windows propriétaire indépendante. PR #35 reste OPEN/DRAFT ; prospective `NOT_STARTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`. Gates : M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`.

## Gouvernance et sources primaires

Exiger **sur le SHA source propre** CI Windows terminale et journaux des tests natifs, diff exact, reviews et threads, règles `Protect main` actives et check strict `Windows frontend and Rust checks` ; squash avec `expected_head_sha`, re-fetch de `main`, nouvelle CI `push` indépendante et issue #38 **append-only**. Un succès CI valide au mieux **ces assertions de fixture**, jamais un ouvreur productif.

- [SQLite `SQLITE_FCNTL_WIN32_GET_HANDLE`](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html) et [SQLite `sqlite3_file_control`](https://www.sqlite.org/c3ref/file_control.html).
- [SQLite VFS `xOpen`](https://www.sqlite.org/vfs.html).
- [Microsoft `BY_HANDLE_FILE_INFORMATION` (FileIndex 64 bits et réserve ReFS)](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information) et [Microsoft `FILE_ID_INFO` 128 bits](https://learn.microsoft.com/fr-fr/windows/win32/api/winbase/ns-winbase-file_id_info).
