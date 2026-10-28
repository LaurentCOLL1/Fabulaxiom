# M3.2 — SQLite VFS Windows : `-wal` via `xOpen`, `-shm` via `xShmMap` (28 octobre 2026)

**STATUT : CANDIDATE STRICTEMENT SOURCE/FIXTURES, NON QUALIFIÉE avant CI Windows exacte.** Base vivante observée : `main=d235e492c5081734ff226563eec6fdb983e4808d` ; PR #201 fusionnée, source `c9b8567f6b1a0c4af44a835ec2fe5f39449193e5`, [CI source #40593808508](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40593808508) et [postmain indépendante #40595455638](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40595455638) SUCCESS (177 Rust / 7 Greenfield / 38 gardes / 132 contrats) ; [issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6455411875). Ces PASS **ne valent pas** pour la candidate présente.

## Surface sous revue

- Le VFS SQLite `sqlite3_vfs.xOpen` reçoit le fichier principal, les journaux rollback et le WAL (`SQLITE_OPEN_WAL`). Refuser l'ouverture du WAL avant délégation est démontrable pour un *fichier jetable*.
- Le WAL-index `-shm` utilise les méthodes `sqlite3_io_methods.xShmMap`, `xShmLock`, `xShmBarrier`, `xShmUnmap` du **fichier principal**. L'interception de `xOpen` seule ne couvre **pas** la création/mapping `-shm` par le VFS Windows délégué. Une vérification de suffixe de nom dans `xOpen` ne donne pas un contrat complet de sidecars.
- Le VFS laboratoire actuel copie le dispatch du VFS Windows et remplace **seulement** `xOpen`, avec nom unique `makeDflt=0`. Il ne substitue pas son propre `sqlite3_io_methods`; aucune chaîne de confiance durable des handles n'est revendiquée.

Références primaires SQLite : [VFS `xOpen`](https://www.sqlite.org/c3ref/vfs.html), [méthodes `xShm*`](https://www.sqlite.org/c3ref/io_methods.html), [format WAL et rôle du WAL-index](https://www.sqlite.org/walformat.html), [mode WAL et mémoire partagée](https://www.sqlite.org/wal.html), [file-control `SET_HANDLE` réservé au débogage](https://www.sqlite.org/c3ref/c_fcntl_begin_atomic_write.html).

## Deux expériences nouvelles, jamais sur le profil opérateur

1. `m32_vfs_fixture_wal_refusal_precedes_named_default_open` : un fichier neuf `create_new(true)` sous répertoire temporaire du runner ; refus `SQLITE_OPEN_WAL` avant délégation ; la transaction fictive échoue sans fichier `-wal` ouvert par ce dispatch.
2. `m32_vfs_fixture_wal_xopen_does_not_cover_shm_mapping` : connexion au même type de fichier jetable, WAL normal et petite table inventée ; le chemin `-wal` est délégué via `xOpen`, le `-shm` est présent tant que la connexion vit, alors qu'aucun nom `-shm` ne traverse le hook `xOpen`. Il s'agit d'un **témoin d'angle mort**, pas d'une politique de durcissement.

Les tests Rust sont exclusivement compilés `#[cfg(all(test, windows))]`, exécutés par les jobs Windows GitHub Actions. Deux nouvelles ouvertures RW sur fixtures uniquement : inventaire textuel `(8,0,0,0,0,9,0)`. Seuils **ATTENDUS, PAS PASS** avant CI de leur SHA : **179 Rust**, **7 Greenfield**, **39 gardes**, **133 contrats**.

## Décision / STOP

Le pré-contrôle FileId128 dans `xOpen` est déjà démontré **non atomique** par #201 ; une future solution doit lier réellement l'identité du handle **effectivement utilisé par SQLite** et médiatiser tous les chemins de fichiers/journaux/WAL/SHM, ainsi que fermer les races de namespace. Ni ce témoin ni les API SQLite documentées ne prouvent la quiescence ou l'absence d'autre writer. `SQLITE_FCNTL_WIN32_SET_HANDLE` n'est **pas** une API d'injection de handle de production.

**Aucun VFS runtime, aucune ouverture de la SQLite v7 du profil unique `com.fabulaxiom.greenfield.v1`, aucune base originale v6, backup, ACL, WAL/SHM/journal/marqueur opérateur, migration 007, IPC writer, CRUD/UX v7 ni Windows Hello natif.** Aucun profil, compte, PIN ou mot de passe d'application supplémentaire. PR #35 OPEN/DRAFT ; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Toute PR : deux prompts, handoffs MD/JSON, protocol/history/roadmaps, CI HEAD exact, diff/reviews/threads, `Protect main`, merge `expected_head_sha`, postmain indépendante, issue #38 append-only.
