# M3.2 — Inventaire élargi des sites SQLite dans tout le Rust Tauri

**SOURCE-ONLY / NON EXÉCUTABLE SUR WINDOWS.** Préparé le 20 octobre 2026 après fusion de [PR #93](https://github.com/LaurentCOLL1/Fabulaxiom/pull/93), `main=15c91039243206dc61190fec5668f32a87f3faf0` au moment du branchement. Nouveau re-fetch avant toute action.

## Pourquoi élargir l'audit de PR #92

L'audit textuel [PR #92](M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md) inspecte six fonctions dans trois modules. Une recherche source-only couvrant les **25 fichiers `.rs` sous `src-tauri/src/`** révèle d'autres sites dans les domaines entités, faits, hiérarchie, révisions, preview M3.1 ainsi que dans les tests et jouets M3.2. Le danger serait qu'un nouveau site `Connection::open` échappe aux contrôles des trois modules précédemment surveillés.

## Garde-fou et limites

Le module `tools/m32_rust_sqlite_open_inventory.py` lit uniquement les fichiers **texte du dépôt de CI** avec `Path.rglob('*.rs')`. Il construit une empreinte d'inventaire fondée sur le **nombre d'occurrences textuelles par fichier** des motifs `Connection::open/open_with_flags/open_in_memory`, `database::open_database`, `run_migrations`, `VACUUM INTO`, `ATTACH DATABASE`, `SQLITE_OPEN_READ_ONLY/READ_WRITE/CREATE/URI`, et certaines API brutes/backup. Les comptes de référence sont figés sur le commit de départ. Toute occurrence ajoutée, supprimée ou déplacée entre fichiers provoque **STOP / relecture** tant que la nouvelle baseline n'a pas été revue.

18 tests en CI vérifient la détection de nouveaux sites Rust, d'un nouveau fichier, de changements de migration et des marqueurs WAL/ATTACH, ainsi que le refus absolu d'autoriser G3. Un fichier neuf sans aucun motif SQLite ne déclenche pas un STOP inutile.

**Ce contrôle n'est PAS un parseur Rust complet.** Il ne comprend pas les macros, les alias d'import ou les appels à nom dynamique, et peut compter des commentaires, chaînes littérales et tests comme du code. Plusieurs changements compensatoires conservant les mêmes totaux peuvent échapper à l'inventaire ; la revue humaine du diff et les gardes des fonctions connues restent indispensables. Les motifs Rust ne sont pas des preuves runtime, ne qualifient pas une absence de writer et ne constituent jamais une autorisation sur les bases de l'opérateur.

## Décision

- G2-A : `PASS_METADATA_ONLY_OWNER_REPORTED` (20 octobre 2026 à 01:31:24 +02:00), autorisation de l'unique essai déjà consommée.
- G2-B/C/D : `NOT_AUTHORIZED` ; G3 réel : `STOP_UNAVAILABLE` ; G4/G5/G6 : `NOT_AUTHORIZED`.
- Absence d'écrivain SQLite : `NOT_PROVEN` ; owner non migrant authentifié : `NOT_ESTABLISHED` ; chaîne historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED`.
- Aucune modification de `src-tauri/src/*.rs`, aucun lancement de Tauri ni de SQLite, aucun accès v6/v7, WAL/SHM/journaux/ACL/sauvegardes/markers, aucune migration 007, IPC writer, fusion PR #35, M3.3 ou release.
- Avant une commande sur le PC de l'opérateur : code intégral, risques et effets, interactions Entrée/`q`/UAC, consentement neuf et séparé.

Références : [SQLite WAL](https://sqlite.org/wal.html), [rusqlite OpenFlags](https://docs.rs/rusqlite/0.40.2/rusqlite/struct.OpenFlags.html), [décision courante](../continuity/M3_2_GATE_DECISION_CURRENT.md).
