# M3.2 — Deux connexions SQLite à la même RAM fictive : preuve négative

**SOURCE-ONLY ET FIXTURES INVENTÉES, CI UNIQUEMENT — PAS DE COMMANDE OPÉRATEUR NI DE DROIT G2-B/G3.**

Checkpoint : 20 octobre 2026, après fusion de [PR #95](https://github.com/LaurentCOLL1/Fabulaxiom/pull/95), `main=a8578b8e128af2264e85a7341a96e13d0e086b23` au départ de la tranche. La CI de `main` #39407869929 a été revérifiée terminale SUCCESS. Re-fetch avant toute écriture/fusion.

## Pourquoi ce test est nécessaire

Les 13 tests Rust de PR #95 valident le refus d'écriture et l'intégrité d'une **connexion déjà ouverte** à une SQLite imaginaire `:memory:` privée. Ils n'ont pas observé un second propriétaire de la même base. Or les garanties sont **propres à la connexion** :

- `PRAGMA query_only=ON` refuse les INSERT/UPDATE/DELETE de la connexion configurée, mais n'empêche pas une autre connexion de modifier les mêmes données. SQLite prévient également que ce PRAGMA n'est pas un verrouillage absolu du fichier.
- `total_changes()` comptabilise les modifications effectuées par **une seule connexion**. La valeur peut rester constante alors que d'autres connexions modifient les données.
- `PRAGMA data_version` peut signaler un changement écrit par une autre connexion entre deux observations. Il ne prouve cependant pas qu'aucun écrivain ne peut agir après l'observation, ni une origine/custodie authentifiée.

## Test entièrement hors disque

`tools/test_m32_shared_ram_other_writer_counterexample.py` utilise la **seule URI figée** :

`file:fabulaxiom_m32_only_fictional_ram_concurrency?mode=memory&cache=shared`

La bibliothèque `sqlite3` de Python l'ouvre avec `uri=True`, en mode RAM partagé. Deux connexions distinctes du même processus CI accèdent à la même base éphémère ; les deux `PRAGMA database_list` doivent donner exactement `main` avec chemin vide. L'ensemble est effacé en fermant les deux connexions. Aucun nom ni chemin fourni par l'opérateur, aucun SQLite v6/v7 original, aucun réseau, aucune sauvegarde, aucun processus Tauri.

La CI exécute douze contre-exemples : base RAM doublement visible, INSERT/UPDATE/DELETE refusés du lecteur, INSERT/UPDATE/DELETE admis sur une deuxième connexion, `total_changes` du lecteur inchangé, `data_version` potentiellement modifiée, `query_only` indépendant, modification de schéma par l'autre connexion, et refus d'autoriser G3 avec tous les indicateurs positifs locaux.

**Ne pas généraliser aux fichiers réels :** ce test ne modélise ni les ACL, ni WAL/SHM, ni journaux de récupération, ni identités de fichiers, ni la durée de vie des handles Windows ; le mode shared-cache RAM est utilisé uniquement pour obtenir un contre-exemple reproductible. Le partage des caches SQLite est déconseillé pour les nouvelles applications, et n'est pas proposé comme architecture de production.

## Décision

Même en cas de 12/12 tests CI SUCCESS : `G2A=PASS_METADATA_ONLY_OWNER_REPORTED` reste borné, `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, `TRUSTED_NONMIGRATING_OWNER=NOT_ESTABLISHED`, `REAL_G3=STOP_UNAVAILABLE`, `G2B/C/D/G3/G4/G5/G6=NOT_AUTHORIZED`. Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Autorisation unique G2-A consommée.

Ne pas ouvrir/modifier les originaux SQLite v6/v7, les sidecars, sauvegardes, ACL, marqueurs, migration 007, writer IPC, PR #35, M3.3 ou release. Une nouvelle procédure Windows demande le code exact complet et un **nouvel accord explicite**.

## Sources officielles

- [SQLite — In-Memory Databases](https://www.sqlite.org/inmemorydb.html)
- [SQLite — PRAGMA query_only, data_version](https://www.sqlite.org/pragma.html)
- [SQLite — Total Number Of Rows Modified](https://www.sqlite.org/c3ref/total_changes.html)
- [SQLite — Shared-Cache Mode](https://www.sqlite.org/sharedcache.html)
