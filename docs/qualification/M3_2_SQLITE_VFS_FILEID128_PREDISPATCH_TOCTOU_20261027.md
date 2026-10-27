# M3.2 — FileId128 dans `sqlite3_vfs.xOpen` : preuve négative de fenêtre TOCTOU

**CANDIDATE NON QUALIFIÉE, SOURCE/FIXTURES Windows UNIQUEMENT.** Baseline vivante du 27 octobre : [PR #200](https://github.com/LaurentCOLL1/Fabulaxiom/pull/200) MERGED, source `6b9ff6351ab5e74661a65fa5b8d895237fc6d4bc`, [CI source #40584565021](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40584565021) SUCCESS (**174 Rust, 7 Greenfield, 37 gardes, 131 contrats**), fusion protégée `main=beda84001ebe6ee2769cb9377017848e52319e70`, [CI postmain #40586436340](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40586436340) SUCCESS indépendante au SHA exact, [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6454165007). Ces PASS historiques ne qualifient pas la présente candidate.

## Hypothèse à réfuter

La PR #200 a testé un refus `SQLITE_OPEN_MAIN_DB` ou `SQLITE_OPEN_MAIN_JOURNAL` **avant** de déléguer `xOpen` au VFS Windows. Cela démontre la position temporelle du callback, **pas** une possession atomique du fichier : même une comparaison FileId faite dans ce callback peut être suivie d'un changement du nom de fichier **avant** l'appel à l'ouvreur Windows distinct.

Cette nouvelle expérience exploite seulement le VFS nommé du module Rust `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs`, **`#[cfg(all(test, windows))]`**, et ses chemins sous racine temporaire CI possédée par le test. L'identité Win32 est le couple **volume 64 bits + FileId 128 bits**, lu sur un handle actif par `GetFileInformationByHandleEx(FileIdInfo)`. Pour observer ce que le VFS a *réellement* ouvert, l'identité du handle SQLite est demandée **après** `xOpen` via `SQLITE_FCNTL_WIN32_GET_HANDLE` ; ce handle est emprunté, jamais fermé/remplacé.

Trois fixtures à qualification fraîche :

1. **Stable** : le callback lit FileId128 sur le fichier de fixture connu, délègue `MAIN_DB`, puis le handle natif SQLite porte le même FileId. Cela atteste uniquement une exécution positive sous nom stable.
2. **Remplacement déjà arrivé** : une ancienne fixture est renommée sous un autre nom encore détenu par la racine, une nouvelle est créée au nom attendu *avant* l'appel SQLite. Le callback refuse le mauvais FileId **avant** délégation ; le compteur de délégations demeure zéro et l'ancienne fixture est intacte.
3. **Course délibérée dans le callback** : FileId128 est comparé et accepté **avant** délégation ; le même callback, en laboratoire seulement, déplace alors l'ancien fichier et crée un nouveau fichier sous le nom attendu ; l'ouvreur Windows délégué reçoit ce nom substitué. Le FileId du vrai handle SQLite est différent de celui qui avait été accepté et correspond au nouveau fichier. **Aucun SQL applicatif n'est exécuté** sur ce handle substitué.

Le troisième cas **réfute un precheck FileId ponctuel comme solution atomique**, y compris lorsque ce precheck est déplacé dans `xOpen`. Le remplacement est contrôlé et délibéré ; il ne prétend ni reproduire un attaquant réel, ni prouver qu'un adversaire peut traverser des handles/partages conservés, ni évaluer les ACL, répertoires ancêtres, junctions/reparse, hard links, WAL/SHM, rollback journals ou écrivains concurrents. Un futur ouvreur productif devra lier **le handle autorisé au handle effectivement utilisé par les opérations de SQLite**, traiter tous les fichiers auxiliaires et obtenir sa propre qualification ; l'opcode `SQLITE_FCNTL_WIN32_SET_HANDLE` n'est pas une solution : SQLite le réserve au débogage et à ses builds de test.

**Cibles explicites, PAS encore PASS :** 177 tests Rust (3 nouveaux), 7 Greenfield inchangés, 38 gardes d'inventaire (nouveau refus textuel), 132 contrats de handoff. Inventaire du module revu de `(3,0,0,0,0,4,0)` vers `(6,0,0,0,0,7,0)`, strictement test-only ; aucune ouverture production supplémentaire, aucune dépendance, aucun script opérateur.

**STOP inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Windows Hello HWND natif non autorisé ; un seul utilisateur Windows et profil `com.fabulaxiom.greenfield.v1`, aucun compte/PIN/mot de passe Fabulaxiom. Aucun accès aux SQLite v6/v7 originales, backups, ACL, journaux, marqueur, migration 007 ou IPC writer ; aucune admission Tauri v7/CRUD/UX.

Après nouvelle CI source au SHA exact : inspecter les trois lignes de témoins Windows, inventaire, handoff, diff/reviews/threads, règle `Protect main` strict active ; protéger la fusion avec `expected_head_sha`, exiger une CI `push` postmain indépendante, puis commenter l'issue #38 en **append-only**. Ne jamais transférer un PASS entre SHAs.

## Sources primaires

- [SQLite, VFS `xOpen` et modes `MAIN_DB`, `MAIN_JOURNAL`, `WAL`](https://www.sqlite.org/c3ref/vfs.html)
- [SQLite, file-control Win32 GET_HANDLE et SET_HANDLE réservé au débogage](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html)
- [Microsoft, `FILE_ID_INFO` volume et identifiant 128 bits](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
