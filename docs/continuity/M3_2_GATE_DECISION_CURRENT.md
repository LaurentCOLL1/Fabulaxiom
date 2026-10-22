# Fabulaxiom M3.2 — Décision de gates au 20 octobre 2026

**22 octobre 2026 — PR #126 protégée MERGED :** HEAD source `0a5f972472eec1e53cd2621ca1fb3d6955e5f18f`, CI [#39727486056](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39727486056) terminale SUCCESS (74 étapes, 132 Rust, 58 handoff et Chromium 50/50 normal et CSP), fusion `main=7c4ff2f84bb67b51c8ca01eef0f9ca78a1bfe8d9`. CI post-main [#39748359823](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39748359823) IN_PROGRESS_AT_CHECKPOINT, re-fetch terminal. Nouvelle tranche candidate React : historique de chaînes de corrections sur des données inventées, huit tests Vitest et 53 cas Chromium chaque mode, non qualifiée tant que nouvelle CI n'est pas terminale SUCCESS. Cette maquette n'est pas montée dans `App.tsx`, aucun accès SQLite, réseau ou IPC.

**STOP inchangé :** M3.2 IN_PROGRESS_NOT_ACCEPTED, absence de vrai writer NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, PR #35 OPEN/DRAFT. Aucune base Windows opérateur, sauvegarde/ACL/sidecar/marqueur, migration 007, writer IPC, M3.3, ComfyUI ni release. Paralléliser uniquement les flux indépendants ; commits et merges séquentiels.


**22 octobre 2026 — PR #125 MERGED sous Protect main :** source `8ce7bb3ae2295662dfba8f4b5961f9394f1e771f`, [CI #39723734278](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39723734278) **SUCCESS** terminale (74 étapes Windows, 132 Rust, 57 contrats, 50/50 Chromium normal et 50/50 CSP), fusion `main=4b14afbc7fe8de607429e795b656179724d7ee7f`. CI post-main [#39726331901](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39726331901) **SUCCESS terminale au SHA exact** au moment de ce commit; re-fetch terminal nécessaire. La tranche Rust de chaînes récursives reste exécutée uniquement par `#[cfg(test)]` et SQLite RAM, aucune fonction Windows livrée.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; absence de writer SQLite réel `NOT_PROVEN`; G2B–G6 `NOT_AUTHORIZED`; vrai G3 `STOP_UNAVAILABLE`; preuves historiques `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; PR #35 historique DRAFT. Aucune commande Windows opérateur, SQLite v6/v7 originale ou backup, ACL/sidecars/marker, migration 007, IPC writer, M3.3, ComfyUI ni release. Paralléliser les travaux indépendants et sérialiser les commits/merges selon `HANDOFF_PROTOCOL.md`.


**22 octobre 2026 — PR #124 MERGED :** source `1fdbe18b163dc8caa48bfde439a36b93b81c848a`, CI [#39721484412](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39721484412) **SUCCESS** (74 étapes Windows, 132 Rust, 56 contrats, Chromium 50/50 normal et 50/50 CSP), fusion `main=db09722076561d35dcc0fe3495e21cf0d0ceef9f`. CI push [#39723495236](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39723495236) `IN_PROGRESS_AT_CHECKPOINT`, re-fetch terminal obligatoire. Septième tranche historique de chaîne récursive en Rust `#[cfg(test)]` et SQLite exclusivement en mémoire, SQL candidat sans migration ni IPC.

**Barrières inchangées :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence d'écrivain réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 historique OPEN/DRAFT. Aucune intervention Windows, bases originales v6/v7, backups/ACL/sidecars/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. Maintenir parallélisme uniquement pour flux indépendants, et séries de commits/merges.


**22 octobre 2026 — PR #123 protégée MERGED :** HEAD source `f72f1dd51d50661af7dfab39f4059e7a25940472`, CI exacte #39719646691 tentative 2 SUCCESS, 74 étapes Windows, 128 tests Rust, 54 contrats de continuité et 50/50 tests Chromium chaque mode. `main=a3c4112b335bba69e3d5d4fa4673ae05f1a57241` ; CI post-main #39720904972 IN_PROGRESS_AT_CHECKPOINT, résultat terminal à re-fetch. Tranche suivante candidate indépendante : `m3_2_recursive_chain_candidate.sql`, `append_chain_correction`, `revoke_chain_correction`, `list_chain_history` et 4 tests adversariaux exclusivement Rust `#[cfg(test)]` + SQLite fictive RAM. Pas d'IPC ou migration automatique.

**STOP inchangé :** M3.2 IN_PROGRESS_NOT_ACCEPTED, absence de writer SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. PR #35 OPEN/DRAFT ; aucun Windows opérateur, SQLite originale v6/v7, backups, ACL/sidecars/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. Paralléliser uniquement les flux indépendants ; commits/merges et gates séquentiels.

**22 octobre 2026 — PR #122 protégée MERGED :** source `1ade25c7b8c500d712c452a08d90ed26a1ffbe89`, [CI #39717330885](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39717330885) **SUCCESS** terminale 74 étapes Windows, 128 Rust et 53 contrats de handoff, fusion `main=52b06099ba0cff0da15fa697b0e2043afc883a00`. [CI post-fusion #39718851557](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39718851557) **SUCCESS terminale au SHA exact**, résultat terminal à re-fetch. Le SQL candidat `m3_2_successor_revocations_candidate.sql` et les méthodes `revoke_successor`/`list_successor_history` sont fusionnés **uniquement sous Rust `#[cfg(test)]` et SQLite RAM**, avec historique append-only, sans chaînes récursives ni migration normale.

**Barrières non levées :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence d'écrivain SQLite réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun travail Windows opérateur, SQLite réelle, backups, ACL/sidecars/marker, migration 007, IPC writer, M3.3, ComfyUI ou release. Continuer les travaux indépendants en parallèle, et sérialiser commits/merges/règles de sécurité.

**Étape suivante autorisée seulement en tests fictifs :** normaliser la CI de PR #122 au SHA exact puis étudier séparément la correction récursive historique PR #35, avec nouvelle branche, fixture RAM, CI nouvelle et aucune promotion des gates réels.


**22 octobre 2026 — PR #121 fusionnée :** HEAD source `6a1a22dedaa4e3d2c302a56959083017578dc7da`, CI exacte [#39713440057](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39713440057) terminale **SUCCESS** (74 étapes, 125 Rust), fusion protégée `main=08caad24e20eae484e94fd084edb487b5c370bd5`, CI push [#39716352685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39716352685) terminale **SUCCESS** sur ce SHA.

**Nouveau candidat Rust source-only :** révocation terminale et append-only du seul successeur permis, SQL `m3_2_successor_revocations_candidate.sql`, `revoke_successor` et `list_successor_history`, trois tests adversariaux supplémentaires en SQLite RAM `#[cfg(test)]`. Cette branche doit obtenir **sa propre nouvelle CI au dernier HEAD** ; ce n'est pas une acceptation produit. Pas de correction récursive ni de chaîne arbitraire.

**STOP maintenu :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; absence d'écrivain réel `NOT_PROVEN` ; G2B–G6 `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; preuves historiques `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED`. Aucune commande opérateur Windows sans autorisation séparée, original SQLite v6/v7, sauvegarde, marqueur, sidecar, ACL, migration 007, writer IPC, M3.3, ComfyUI ou release. Paralléliser seulement des tâches indépendantes et garder les writes/merges séquentiels.


**22 octobre 2026 — PR #120 fusionnée :** source HEAD `f7ef3ceeaee40bb90e1cb9fe180121f11867fc28`, [CI PR #39685054113](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39685054113) **SUCCESS terminale** (74 étapes Windows), fusion protégée `main=01766707a347a269b283c2aa7ea02f44979759e9`, [CI post-fusion #39686405108](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39686405108) **SUCCESS terminale au SHA exact**. Le cinquième module Rust de chronologie reste strictement `#[cfg(test)]`, utilise SQLite RAM et démontre un **successeur humain unique** après retrait d'une reformulation, avec graphe actif en ordre partiel. Aucun code de production/IPC n'est activé.

**Aucune promotion des gates :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT non fusionnable, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, attestations historiques `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Aucun accès opérateur Windows, SQLite v6/v7 originale, backup, ACL, WAL/SHM, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release. Parallélisation autorisée pour lectures et travaux indépendants, mais commits sur même branche et merges séquentiels avec CI SHA exact.


**22 octobre 2026 — PR #119 MERGED sous Protect main :** source `0df96696e4abefe692f8a0fdca3ab10e726fa9d3`, CI PR #39661776335 SUCCESS (74 étapes, 121 tests Rust, 48 tests continuité, 21 inventaires SQLite, 50 Chromium par mode). Nouveau `main=61e07deaf10fc393c567e8f1960874b75d81adc4`, CI post-fusion #39684342539 **IN_PROGRESS_AT_CHECKPOINT** ; revérifier le résultat terminal au SHA exact.

**Cinquième tranche test-only candidate :** un successeur humain unique d'une reformulation retirée, `succeed_withdrawn_restatement`, lecture du graphe actif partiel par `list_active_precedence_graph` et SQL candidat `m3_2_restatement_successors_candidate.sql` sur SQLite exclusivement en RAM. Quatre nouveaux tests Rust : retrait obligatoire, unicité, cycles/doublons, ancres retirées et historique immuable. Aucune correction en chaîne, aucune révocation de successeur, aucune inférence de chronologie totale.

**STOP non levé :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Pas de Windows opérateur, SQLite originale v6/v7, backups, ACL, sidecars, marker, migration 007, writer IPC, M3.3, ComfyUI ou release.


**21 octobre 2026 — PR #118 MERGED :** source `ff996fc27da6df12697d68a46b8580a3a33e30b3`, CI #39658544037 SUCCESS (74 étapes, 117 Rust, 46 contrats, 21 inventaires SQLite, 50 Chromium par mode), fusion protégée `main=a0942b9566d6de21cf73e55dce47c3797dcb7c81`. CI push #39660168071 **IN_PROGRESS_AT_CHECKPOINT** : ne pas prétendre sa réussite terminale sans re-fetch exact. Nouvelle tranche test-only, uniquement SQLite RAM : révocation immuable de reformulation, historique conservé, 4 tests Rust supplémentaires ; aucune écriture active supplémentaire déduite.
**STOP toujours effectif :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, réel writer NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique 21/3/2 PENDING_EXTERNAL_ATTESTATION, prospective NOT_STARTED. Pas de Windows opérateur, original SQLite v6/v7, backup, ACL, journal, marker, migration 007, IPC writer, M3.3 ni release.


**Revalidation publique 21/10/2026 :** PR #117 MERGED à `b76e6c00c579bee36c194872e3679c48fe9788fa`, CI push #39655214998 SUCCESS. La prochaine tranche de reformulation explicite reste confinée aux bases SQLite RAM et ne prouve aucun état opérateur ni autorisation G2-B–G6.



**Revalidation source publique au 21/10/2026 :** PR #116 MERGED `388cb745888f9f2d4d0a07fce1ed19fad9b4a548`, push CI #39628479487 SUCCESS au SHA exact. Les décisions Rust + SQL candidates de la prochaine tranche restent exclusivement dans des tests SQLite en RAM ; cette preuve ne modifie aucun statut de G2A/G2B–G6.

**Checkpoint public du 21/10/2026, sans ouvrir les gates :** PR #115 MERGED, CI push #39620942276 SUCCESS sur `33846c8c6813acda5eda5089827f81df99175d2c`. Un portage `#[cfg(test)]` sur SQLite en RAM n'authentifie aucun fichier opérateur. G2B–G6 restent NOT_AUTHORIZED ; aucun changement du tableau de décision ci-dessous.


**Actualisation des sources publiques du 21/10/2026, pas décision opérateur :** PR #114 MERGED `ddb23311f40f09c04983b164ccd7afa361698ea8`, CI post-merge #39614175650 SUCCESS sur SHA exact. Le document de gates décrit toujours le résultat opérateur daté du 20/10 : aucune promotion. Des chantiers source-only parallèles sont décrits dans [le plan de réconciliation](../qualification/M3_2_PR35_SAFE_RECONCILIATION_PLAN.md) et [le protocole permanent](HANDOFF_PROTOCOL.md).

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
