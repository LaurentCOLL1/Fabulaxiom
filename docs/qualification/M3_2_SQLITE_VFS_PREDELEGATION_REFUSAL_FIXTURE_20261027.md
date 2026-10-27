# M3.2 — frontière `sqlite3_vfs.xOpen` avant délégation, témoin Windows jetable

**CANDIDATE SOURCE/FIXTURES UNIQUEMENT, NON QUALIFIÉE.** Base : [PR #199](https://github.com/LaurentCOLL1/Fabulaxiom/pull/199) MERGED, source `debc6f9cea8ba668f64afd9c815445c282c842c4`, [CI source #40576413834](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40576413834) SUCCESS (171 Rust, 7 Greenfield, 36 gardes, 130 contrats), `main=4e04412b1d4cbdb4ce738b32c8a06c2ab6127b61`, [postmain #40578342548](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40578342548) SUCCESS indépendante, [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6453334855). Ces CI **ne qualifient pas** la présente candidate.

## Question, mécanisme, périmètre

Le contrôle Win32 de l'identité 128 bits de `main` via `SQLITE_FCNTL_WIN32_GET_HANDLE` s'exécute **après** le `xOpen` du VFS SQLite. La comparaison, même positive, ne prouve ni ouverture atomique, ni absence d'effets I/O déjà intervenus, ni chaîne de confiance des sidecars. Le contrat officiel du VFS précise que `xOpen` reçoit `SQLITE_OPEN_MAIN_DB`, `SQLITE_OPEN_MAIN_JOURNAL`, `SQLITE_OPEN_WAL`, etc. Un refus dans le callback **avant délégation à l'ouvreur OS** peut donc être observé sans confondre une comparaison post-ouverte avec une admission préalable.

Le module `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs` est compilé **uniquement** en `#[cfg(all(test, windows))]`. Une instance nommée unique de `sqlite3_vfs` copie le dispatch Windows existant, remplace **seulement `xOpen`**, conserve `pAppData`, n'est **jamais VFS par défaut** (`makeDflt=0`) et se désinscrit à la fin du test. Le callback remet `sqlite3_file.pMethods=NULL` au refus, selon le contrat SQLite. Aucune registration ni opération de ce laboratoire n'est présente dans le runtime Tauri.

Trois expériences sont prévues dans des répertoires de test nouvellement créés sous `%TEMP%` du runner :

1. Refuser `SQLITE_OPEN_MAIN_DB` **avant** la délégation et vérifier que `Connection::open_with_flags_and_vfs` échoue, que le compteur de délégations reste à zéro et qu'aucun fichier SQLite n'est créé.
2. Revendiquer exclusivement un nom de fixture par `create_new(true)`, puis autoriser le `xOpen` `READ_WRITE` SQLite explicitement sélectionné ; vérifier une lecture `SELECT 1` et le nombre de délégations. C'est un témoin **positif fonctionnel**, nullement une admission résistante à la course des ancêtres.
3. Refuser `SQLITE_OPEN_MAIN_JOURNAL` avant délégation pendant une écriture sur SQLite jetable en mode rollback `DELETE`, vérifier l'échec de la transaction et l'absence de journal créé par l'ouvreur délégué. L'accès aux autres sous-systèmes (`xAccess`, `xDelete`, WAL/SHM, locks, reparse, ancêtres, ACL) reste **hors preuve**.

**Cibles, pas PASS avant CI exacte** : 174 Rust (3 Windows supplémentaires), 7 Greenfield, 37 gardes d'inventaire, 131 contrats de continuité. L'inventaire textuel a été élargi pour détecter `Connection::open_with_flags_and_vfs`, avec occurrence nouvelle revue `(3,0,0,0,0,4,0)` ; ce n'est pas une analyse formelle de la sécurité du code.

## Critère de décision et STOP

Même si les trois tests passent en CI Windows, le proxy **ne réutilise pas un handle CreateFile authentifié**, ne garantit aucune absence de substitution entre admission et l'ouvreur Windows, n'authentifie ni ancêtres, ni sidecars, ni namespace d'origine, ni writer. Il ne constitue donc **PAS un ouvreur v7 atomique**, un gate G2B, ni une autorisation de CRUD/UX réelle. Il indique seulement **où** un futur contrôle pré-`xOpen` devra intervenir et que les fichiers auxiliaires exigent un gate distinct. Un wrapper de production nécessiterait la conception complète de la sémantique VFS/IO et des handles, une politique de sidecars/WAL/SHM, une preuve de possession et un audit séparé.

Aucun Windows de Laurent, aucune SQLite v6/v7 originale, backup, ACL, journal, sidecar, marqueur opérateur, migration 007, IPC writer ou dialogue Hello natif n'est ouvert ou modifié. Profil unique `com.fabulaxiom.greenfield.v1`, pas de compte/PIN/mot de passe. L'activation native Hello HWND requiert une autorisation distincte. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT.

CI au **nouveau SHA source exact**, lecture diff/reviews/threads, contrôle requis et `Protect main` actif/strict, fusion `expected_head_sha`, nouvelle CI postmain **indépendante** puis issue #38 append-only. Aucune qualification héritée des anciennes CI.

## Sources normatives

- [SQLite — contrat `sqlite3_vfs`/`xOpen`, `pMethods`, flags main/journal/WAL](https://www.sqlite.org/c3ref/vfs.html)
- [SQLite — enregistrement et sélection d'un VFS nommé](https://www.sqlite.org/c3ref/vfs_find.html)
- [SQLite — `SQLITE_FCNTL_WIN32_GET_HANDLE` est une observation du handle ouvert](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html)
- [SQLite — `SQLITE_OPEN_EXCLUSIVE` n'est pas un verrou d'accès pour `sqlite3_open_v2`](https://www.sqlite.org/c3ref/c_open_autoproxy.html)
