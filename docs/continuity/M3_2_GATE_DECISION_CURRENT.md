# Fabulaxiom M3.2 — Décision de gates au 20 octobre 2026

**Revalidation documentaire du 21 octobre 2026, sans ouverture de gate :** PR #113 fusionnée sous Protect main à `e74f1001c01eff1f37c8b35d97d4ef34f6fbccb3` et CI post-fusion #39607280677 SUCCESS au SHA exact. Parallélisation des recherches, tests fictifs et lectures de source autorisée selon [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) ; **aucune** opération G2-B–G6 ni aucune autorisation implicite supplémentaire. La matrice G2-A/G2-B–G6 ci-dessous décrit toujours les gates observés au 20 octobre et reste inchangée.

**ÉTAT DATÉ DOCUMENTAIRE, NON EXÉCUTABLE.** Re-fetch GitHub requis. Ce fichier n'est ni une autorisation locale ni une preuve indépendante. Lire avec `HANDOFF_CURRENT.md` et le snapshot historique daté du 19 octobre.

## Résultats réels, distincts des tests CI

| Étape | État au 20 octobre | Portée et raison |
| --- | --- | --- |
| G2-A — observation processus Windows | **PASS_METADATA_ONLY_OWNER_REPORTED** | Une seule exécution spécifiquement autorisée le 20 octobre à 01:31:24 +02:00 : token MEDIUM, six processus WebView2 descendants du nom SearchHost. Sortie déclarée par propriétaire, non attestée indépendamment. Autorisation consommée. |
| G2-B, G2-C, G2-D | **NOT_AUTHORIZED** | Aucun accord neuf, aucune conclusion sur l'absence d'un écrivain SQLite ou identité du binaire SearchHost. |
| G3 — capture réelle | **STOP_UNAVAILABLE / NOT_AUTHORIZED** | Origine et propriétaire SQLite non migrant non authentifiés ; protocole de source froide, journaux et quiescence non établi. |
| G4 — validation/restauration réelle | **NOT_AUTHORIZED** | Aucune nouvelle capture G3 autorisée ni copie prospective qualifiée. |
| G5 — acceptation de risque par propriétaire | **NOT_AUTHORIZED** | Pas de dossier G4 vérifié et pas de nouvelle baseline prospective. |
| G6 — premier runtime isolé | **NOT_AUTHORIZED** | Runtime Tauri/WebView2 v7 non qualifié ; PR #35 toujours ouverte en brouillon. |
| Migration 007, writer IPC, fusion PR #35, M3.3, release | **NOT_AUTHORIZED** | Pas de promotion par code, par rapport CI ou par ce document. |

## Provenance distincte de G2-A

- Chaîne historique : **PENDING_EXTERNAL_ATTESTATION(21/3/2)** : 21 rôles ancrés, trois observés par SHA-256 seulement, deux non ancrés. Les cinq rôles en question restent listés dans l'issue #36.
- Baseline prospective : **NOT_STARTED**, même si la politique SOLO_OPERATOR_COMPENSATING_CONTROLS est adoptée au niveau documentaire. Aucune signature d'un relecteur indépendant n'est supposée.
- Un PASS G2-A sur les métadonnées **ne répare pas** l'historique et ne crée pas une nouvelle baseline.

## Pourquoi le risque d'écriture reste bloquant

- `database::open_database` utilise `Connection::open` (rusqlite : ouverture en lecture-écriture et création possible) puis `run_migrations`; `database_status` et `create_backup` y font appel. Ne pas les exécuter sur les SQLite protégées.
- La présence ou l'absence de fichiers `-wal`, `-shm` ou `-journal`, un hash stable ou les noms de processus observés ne démontrent pas seuls l'absence d'écrivain concurrent.
- PR #91 : 13 tests fictifs de preuves insuffisantes. PR #92 : 18 tests source-only portant sur six chemins Rust connus. Les suites CI réussies attestent ces règles **sur code public et fixtures**, pas l'état des disques de l'opérateur.

## Reprise concrète sans accès privé

1. Conserver l'ancienne photographie `M3_2_GATE_SNAPSHOT.md/json` comme référence **datée du 19 octobre**, sans réécrire rétrospectivement les décisions d'alors.
2. Préserver la preuve G2-A déclarée et les deux rapports source-only `M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md` et `M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md`.
3. Définir, sur papier et sur fixtures, un mécanisme vérifiable de provenance, de propriétaire non migrant ou de source froide, en reconnaissant que **ni voie A ni voie B n'est actuellement qualifiée**. Ne pas accumuler des contrôles négatifs en les assimilant à une nouvelle autorisation.
4. Pour tout geste futur sur Windows (y compris une simple nouvelle observation G2-B), présenter un script exact distinct, effets sur disque/journaux/réseau, UAC, Entrée/`q` et les conditions STOP ; recueillir une nouvelle autorisation explicite du propriétaire **avant exécution**.

**Originaux interdits :** production restaurée v6, v7 isolée, sidecars, ACL, backups, activation marker et worktrees locaux ; aucune migration 007, aucun IPC writer ni release. Aucun processus Windows n'a été lancé/arrêté et aucune base privée ouverte pour préparer cette décision.

**Références :** [Runbook prospectif NON EXÉCUTABLE](../qualification/M3_2_PROSPECTIVE_BASELINE_WINDOWS_RUNBOOK_DRAFT.md), [issue #36](https://github.com/LaurentCOLL1/Fabulaxiom/issues/36), [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38), [SQLite WAL](https://www.sqlite.org/wal.html), [rusqlite Connection 0.40.2](https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html).
