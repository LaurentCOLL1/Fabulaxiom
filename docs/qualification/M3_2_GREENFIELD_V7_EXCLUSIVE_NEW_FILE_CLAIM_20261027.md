# M3.2 — réservation exclusive d'un nom SQLite v7 neuf, tests de refus CI

Date : 27 octobre 2026. **SOURCE/TEST UNIQUEMENT, NON QUALIFIÉ AVANT SA CI SHA EXACTE.** Base vivante PR #191, source `c6b23ae071392c5f68912e53915df5067787605b`, CI #40469481613 `SUCCESS` (144 Rust), squash protégé `main=2b4a7aaa37b2ada590a8e05fc4c5e973949041cc`, postmain indépendante #40470700689 `SUCCESS`, issue #38 commentaire terminal #6436913166. Ces CI sont historiques par rapport à cette nouvelle candidate.

## Risque traité

Le simple drapeau SQLite `SQLITE_OPEN_CREATE` **n'est pas un garde de création exclusive** : SQLite peut rouvrir un fichier existant. Pour un chemin de *création*, il faut refuser le nom occupé **avant** de demander à SQLite de l'ouvrir. [Documentation officielle SQLite : `sqlite3_open_v2`](https://www.sqlite.org/c3ref/open.html). Ce contrôle est nécessaire, mais insuffisant pour qualifier un chemin opérateur (course au renommage, propriété réelle de l'arborescence, ouverture concurrente externe et identité d'activation non démontrées).

## Code proposé, uniquement `#[cfg(test)]`

Dans `src-tauri/src/world_time_file_migration_tests.rs`, `open_new_only_disposable_file` est appelé **exclusivement sur les noms choisis par les fixtures dans une racine temporaire qu'elles viennent de créer**. Il :

1. Refuse un parent non existant au lieu de le fabriquer implicitement ; refuse les noms annexes déjà occupés `-wal`, `-shm`, `-journal` ; toute erreur d'inspection autre que `NotFound` est un STOP.
2. Réserve le nom au niveau système avec `std::fs::OpenOptions::create_new(true)` (échec si fichier ou dossier préexistant), ferme ce handle puis ouvre **ce fichier neuf seulement** avec `Connection::open_with_flags(..., SQLITE_OPEN_READ_WRITE)` sans `SQLITE_OPEN_CREATE` et configure les clés étrangères.
3. Vérifie les refus sur une ancienne base v6 saine, un fichier arbitraire, un dossier, un parent inexistant, et chacun des trois annexes orphelins ; compare les octets de la v6, du fichier arbitraire, du marqueur fictif et des annexes avant/après.
4. Sur un autre nom libre, installe les migrations automatiques v1–v6 existantes **uniquement dans le fichier neuf**, applique les candidates M3.1 v7 et décisions M3.2 dans une transaction, simule la ligne v7 dans le ledger **de fixture seulement**, écrit une ancre inconnue fictive, ferme/réouvre le fichier connu, vérifie l'intégrité, puis refuse une seconde tentative de *création* sur ce même nom.
5. Lance deux créateurs concurrents sur un troisième nom de fixture et exige **exactement un succès** de revendication.

À qualifier : 3 tests Rust additionnels (total cible **147** depuis le dernier 144 validé), 28 tests source de l'inventaire SQLite, 122 contrats de reprise. Ces nombres sont des **cibles, non des PASS présumés** avant CI.

## Limites non négociables

Le transfert entre le handle OS et la connexion SQLite **n'est pas prouvé race-free contre un adversaire** ; aucun parent de destination opérateur, handle identité OS, IPC Tauri, parcours UI, politique de rechargement, migration automatique 007 ni sauvegarde/restauration Windows n'est qualifié par cette candidate. Ce n'est **pas** l'ouvreur de production v7. Ne pas l'appliquer à `%LOCALAPPDATA%`, à un chemin venant de l'UI ou à un dossier historique. Conserver le profil existant `com.fabulaxiom.greenfield.v1`, aucune destination/profil Tauri supplémentaire.

**Suite après CI exacte et fusion protégée :** concevoir une preuve de propriété/identité de la racine et un handoff sans substitution de chemin, au sein du profil **existant**, puis intégrer l'ouvreur v7 réel et les opérations métier/UX de chronologie dans un nouveau gate explicitement revu. Avant toute opération Windows opérateur, vérifier les protocoles de sauvegarde, refus et relance, et disposer des autorisations/gates séparés pour migration 007 ou IPC writer, qui restent exclus ici.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; writer historique `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 `OPEN/DRAFT`, non fusionnable. Aucune attestation indépendante sur Windows. Toute commande PowerShell destinée à l'opérateur reste entièrement encapsulée dans `& { ... }`. Issue #38 append-only ; `Protect main` et `expected_head_sha` obligatoires, puis CI postmain au squash indépendante.
