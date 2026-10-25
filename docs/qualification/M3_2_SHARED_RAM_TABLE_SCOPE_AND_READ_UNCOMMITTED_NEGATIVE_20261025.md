# M3.2 — Portée des verrous de table et isolation shared-cache fictives (25 octobre 2026)

**SYNTHETIC_TEST_ONLY.** Deux contre-exemples Rust sur des données totalement inventées en RAM. **Aucune procédure opérateur**, aucune preuve sur une base Windows, aucun G3 réel.

## Checkpoint terminal indépendant déjà établi

[PR #175](https://github.com/LaurentCOLL1/Fabulaxiom/pull/175) MERGED par squash protégé après [CI source #40209991293](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40209991293) `completed/SUCCESS` sur `bd5e8ef35b80d653530f1f36d288724c1642f2ea` ; `main=c7d93dd2844bdd3cb17c5ffb5cc600902f9ba18f` avec [postmain indépendante #40210737724](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40210737724) `completed/SUCCESS` à ce SHA. Source : 81/81 étapes Windows ; postmain : 80 réussies, 1 ignorée normalement car propre aux PR, 0 échec. Logs : 109 contrats, 96 Vitest fictifs, Chromium 82/82 dans chaque mode, 132 Rust de base, `toy_20` et `toy_21` PASS. [Checkpoint append-only #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6400147200). Ce succès ne transfère aucune preuve à la présente candidate.

## Deux expériences nouvelles — toujours non qualifiées jusqu'à leur CI

`src-tauri/src/m32_preopened_query_only_toy.rs`, seulement sous `#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]` depuis `lib.rs`. Réemploi de la fabrique **préexistante** `invented_shared_ram_pair`, dont l'URI `file:m32-invented-foreign-writer-<id>?mode=memory&cache=shared` ne crée aucun fichier disque. Chaque test reçoit un nom RAM distinct, sans dépendance à l'OS opérateur.

- **`toy_22_shared_ram_read_lock_is_table_scoped_not_database_wide`** : construire une deuxième table **purement inventée** avant `BEGIN DEFERRED TRANSACTION` du lecteur ; après un `SELECT` verrouillant `imaginary_events`, un autre handle réussit l'`UPDATE` de `imaginary_other_events`, tandis que l'`UPDATE` de la table observée échoue explicitement avec `DatabaseLocked` / `SQLITE_LOCKED`. Libération de cette transaction fictive seulement par `ROLLBACK`. Cela réfute toute assimilation d'un verrou *de table* à une absence d'écrivain pour toute la base.
- **`toy_23_read_uncommitted_does_not_hold_shared_ram_table_read_lock`** : sur une autre base RAM inventée, `PRAGMA read_uncommitted=ON` est établi avant `BEGIN DEFERRED TRANSACTION` ; le `SELECT` n'obtient pas le verrou de lecture standard, un `UPDATE` tierce **sur cette même table fictive** réussit et la nouvelle lecture voit la valeur modifiée. Ici encore, `ROLLBACK` ne concerne que la RAM inventée.

La [documentation officielle SQLite shared-cache](https://www.sqlite.org/sharedcache.html) définit des verrous *par table*, explique l'exception `read_uncommitted` et **déconseille** ce mode pour les nouveaux usages ; cela n'est pas une architecture proposée pour Fabulaxiom. Ni la démonstration du verrou temporaire `toy_21`, ni l'un de ces contre-exemples ne permettent d'inférer les garanties d'une autre configuration (WAL/rollback, autre processus, Windows, connexion propriétaire ou source originale).

## Inventaire, portée et STOP

Aucun nouveau `Connection::open` / `open_with_flags` ; aucune révision des seuils de l'inventaire SQLite, aucun runtime production, Tauri IPC, migration 007, fichier disque, chemin privé, commande PowerShell opérateur, sauvegarde, ACL, marqueur ni journal d'original. Le contrat #110 verrouille la provenance du checkpoint #175, les noms et assertions de ces tests et le refus d'élévation des gates. La CI **source du HEAD candidat exact** puis une CI **postmain indépendante** seront nécessaires après revue du diff, reviews, threads, ruleset et squash `expected_head_sha`.

**STOP :** G2-A `PASS_METADATA_ONLY_OWNER_REPORTED`, B0/B1 `OBSERVED_PARTIAL_ONLY_OWNER_REPORTED` et consentements consommés ; G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT, Linux GLib `OPEN_NOT_REMEDIATED`.

**PAS une attestation historique, une preuve d'absence d'écrivain ou une autorisation opérateur.**
