# M3.2 — Source-only audit des entrées SQLite migrantes et G3

**PAS DE COMMANDE WINDOWS, PAS DE CONNEXION AUX BASES, PAS D'AUTORISATION G3.**
Checkpoint initial après fusion de PR #91 : main fb4625450439ecf236cc9065f434eda002f71533. Re-fetch GitHub obligatoire avant toute action.

## Constat de l'architecture actuelle

Le bloc G2-A PID 0 a retourné **PASS de métadonnées** avec l'accord exprès de l'opérateur, mais l'absence d'écrivain SQLite n'est **pas prouvée** (PROCESS_WRITER_ABSENCE: NOT_PROVEN). La [matrice de la PR #91](M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md) distingue les observations instantanées des garanties de sécurité.

Le contrat public de **rusqlite 0.40.2** précise que Connection::open(path) utilise par défaut SQLITE_OPEN_READ_WRITE, SQLITE_OPEN_CREATE, SQLITE_OPEN_URI et SQLITE_OPEN_NO_MUTEX. Une telle ouverture peut créer la base avant même une migration. Elle n'est pas une voie de lecture neutre de fichiers protégés. Référence officielle : https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html .

## Inventaire des points d'entrée existants

| Fonction dans le dépôt | Risques identifiés par lecture du code public | Verdict G3 sur originaux v6/v7 |
| --- | --- | --- |
| src-tauri/src/database.rs : open_database | Crée potentiellement le répertoire, appelle Connection::open, configure_connection et run_migrations | **VETO** : ouvre/crée et migre |
| src-tauri/src/lib.rs : database_status | Appelle database_path et open_database | **VETO** : le nom « status » n'implique pas une lecture neutre |
| src-tauri/src/backup.rs : create_backup | Appelle open_database sur source et vacuum_copy | **VETO** : accès source migrant |
| src-tauri/src/backup.rs : vacuum_copy | Exécute VACUUM INTO et valide la copie | Ne qualifie pas de capture G3 |
| src-tauri/src/backup.rs : reserve_unique_file | Crée un nouveau fichier puis ferme la réservation avant l'ouverture SQLite | Risque de fenêtre de substitution entre réservation et accès |
| src-tauri/src/backup.rs : read_validated_database | Ouvre avec SQLITE_OPEN_READ_ONLY | Lecture logique uniquement ; le comportement des journaux WAL et des sidecars n'est pas attesté |

## Garde-fou introduit

Le nouveau module **tools/m32_g3_runtime_entrypoint_source_audit.py** lit trois fichiers Rust **publics et versionnés** dans ce dépôt. Il vérifie les séquences **actuellement** identifiées, et retourne toujours un refus réel de G3. Les 18 tests de **tools/test_m32_g3_runtime_entrypoint_source_audit.py** comprennent des mutations de signatures, d'appels de migration, d'ouverture, de VACUUM INTO, de réservation et d'option READ_ONLY. Toute divergence doit provoquer une nouvelle revue ; même une amélioration du code exigera une qualification différente au HEAD nouveau.

**Limite fondamentale :** c'est un contrôle textuel d'un ensemble connu de fonctions ; il n'est ni un parseur Rust complet, ni un graphe exhaustif, ni une preuve d'absence de nouveau point d'entrée, ni un audit runtime, ni une autorité de sécurité. Le PASS de ce contrôle ne peut jamais déverrouiller G3. Aucun fichier privé, WAL/SHM/journal, ACL, backup, marqueur ou worktree de l'opérateur n'a été ouvert.

## Voies futures toujours non établies

- **Owner déjà ouvert non migrant, authentifié et révocable** : non disponible sur les originaux réels ; des fixtures RAM n'en prouvent pas l'existence.
- **Source froide réellement quiescente** : identité et chaîne historique de conservation, ancêtres, sidecars/journaux et verrouillage continu à prouver avant tout accès.
- **Publication de copie dans un nouveau répertoire et restauration tierce** : aucune procédure G3 réelle autorisée ; une réservation ponctuelle ne suffit pas à établir l'absence de substitution.
- **Accord du propriétaire** : toute nouvelle commande Windows doit être fournie intégralement avec effets (Entrée/q/UAC/disque/réseau), puis faire l'objet d'un accord exprès distinct.

**Statuts :** G2-A PASS_METADATA_ONLY_OWNER_REPORTED ; PROCESS_WRITER_ABSENCE NOT_PROVEN ; provenance PENDING_EXTERNAL_ATTESTATION(21/3/2) ; baseline prospective NOT_STARTED ; G2-B/G2-C/G2-D et G3–G6 NOT_AUTHORIZED ; REAL_G3 STOP_UNAVAILABLE ; PR #35 DRAFT, issues #36/#38 ouvertes. Pas d'original v6/v7, sidecar, backup, migration 007, IPC writer, M3.3 ou release.

## Sources publiques

- https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html
- https://www.sqlite.org/wal.html
- https://www.sqlite.org/uri.html
- https://www.sqlite.org/backup.html
