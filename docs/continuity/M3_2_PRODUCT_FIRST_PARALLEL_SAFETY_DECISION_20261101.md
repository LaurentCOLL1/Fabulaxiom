# M3.2 — Décision de priorité PRODUIT D'ABORD / SÉCURITÉ EN PARALLÈLE

**Date : 1er novembre 2026. Statut de la décision : CHOIX EXPLICITE DU PROPRIÉTAIRE, ACTIF ET RÉVERSIBLE.**
Autorité : demande de l'utilisateur du 1er novembre 2026, après revue du progrès estimé de M3.2. La présente décision prime sur les anciens plans de séquencement **pour l'ORDRE DES TRAVAUX uniquement** ; elle n'annule, ne modifie et ne satisfait AUCUN gate de sécurité ni exigence d'acceptation. Re-fetch GitHub vivant avant toute action ; la dernière autorité source connue à la création est `main=df7171ac99c9f0a6a5e9123de2c8c8168cfb7090`, PR #256 fusionnée, CI Windows source #41308216274 et postmain #41309028506 TERMINALES SUCCESS (294/7/67/177).

## Objectif et choix opératoire

**Priorité principale : livrer une chronologie M3.2 manuelle, locale, réellement utilisable dans Fabulaxiom.** Avancer en parallèle sur deux pistes, par PR petites et vérifiables :

- **PISTE PRODUIT — prioritaire pour l'effort d'intégration :** faire converger le schéma v7 existant, `m32_manual_chronology.rs` (actuellement `#[cfg(test)]`), les composants React de chronologie fictive et le service Rust préparé `m32_v7_writer_service.rs` (non câblé) vers un parcours vertical concret **sur fixtures v7 entièrement neuves et jetables** : créer/consulter/corriger/révoquer une ancre temporelle ; créer une relation avant/après ; refuser cycles, références inter-Univers et faux ordre total ; consulter l'ordre du monde indépendamment de l'ordre de narration et de révélation. Identifier clairement la persistance **réelle sur fixture** et distinguer mock, RAM et disque. D'abord sans Ollama, cloud, modèle payant ni publication de release.
- **PISTE SÉCURITÉ — toujours obligatoire, mais non bloquante pour prototypes sûrs et isolés :** continuer R4 (toutes régions xShmMap, identité et durée de vie HANDLE main/-wal/-shm non atomiques aujourd'hui), puis R5/R6/R8 et R7/R9, preuves de source/écrivains et conservation. **La piste produit ne peut JAMAIS traverser une barrière de sécurité non satisfaite.** Les travaux hors runtime, sur nouvelles fixtures, n'authentifient ni ne remplacent une admission d'ancienne base ni une attestation indépendante.

**Pas de nouveau profil permanent ni d'autre utilisateur.** Pour les démonstrateurs v7, uniquement des répertoires `%TEMP%` créés exclusivement pour le test via `CREATE_NEW` et nettoyés par le test. L'application réelle et le profil local existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` restent strictement hors périmètre jusqu'à admission et validation distinctes. `M:\Fabulaxiom` est un emplacement du dépôt de développement, pas une source de bases de test GitHub.

## Séquencement concret à suivre dans LES PROCHAINES CONVERSATIONS

| Ordre | Tranche vérifiable | Livrable et test d'arrêt |
| --- | --- | --- |
| P0 | Matrice exigences → code → tests, sans écrire dans une base privée | Lister ce qui existe déjà : `m32_manual_chronology.rs`, v7/M3.1, composants fictifs React, service writer Rust déjà préparé ; ne pas fusionner la vieille PR #35 en bloc. |
| P1 | **Vertical slice v7 sur fixture neuve** | Tester création + consultation d'ancre exacte/relative/inconnue et lien avant/après sur un nouveau fichier SQLite v7 dans un `%TEMP%` de CI, fermeture puis réouverture du **même fichier inventé** ; vérifier références de scènes/révisions, deux Univers et plusieurs romans, rejet inter-Univers/cycle, absence de mutation de données réelles. Aucun Tauri IPC production. |
| P2 | Reprise/adaptation du service Rust existant | Commandes typées limitées à la fixture propriétaire déjà ouverte, refus sur source non admise, transaction bornée et preuves de conservation ; pas de constructeur `V7WriterAdmission` en runtime ni API de production. |
| P3 | Atelier React/Tauri isolé et testable | Par défaut, aperçu sur données inventées sans persistance trompeuse ; si ouverture SQLite v7 jetable, marqueur **test-only** explicite, interface non montée dans l'app opérateur, aucune réutilisation d'un profil privé ; tester E2E et indiquer clairement les limites. |
| P4 | Gate d'admission réelle (séparé) | Réévaluer R4–R9, provenance, historique/prospective, backups, writer tiers, garde d'identité atomique, IPC/Hello et consentement ; impossible de lever ce gate par des tests CI fictifs. |
| P5 | Acceptation Windows utilisateur puis normalisation | CRUD chrono persistant et interface opérateur sur profil admis seulement après P4, intégrité v6/v7 et sauvegardes vérifiées, puis CI SHA exact, PR protégée et normalisation indépendante. |

**Rythme :** consacrer les prochaines PR à de petits incréments de la piste PRODUIT (P0→P3), avec des contrôles nécessaires sur la piste SÉCURITÉ en parallèle, plutôt qu'à une succession exclusive de « toys » Win32. Prochaine PR de code recommandée : P1, preuve create/list/reopen v7 sur `CREATE_NEW` `%TEMP%`, réutilisation des modules existants ; ne pas recoder le moteur d'événements complet. Documenter chaque tranche obtenue vs non obtenue.

## Conditions qui imposent de réévaluer la stratégie ET D'EN INFORMER L'UTILISATEUR

**Ne pas changer silencieusement la priorité.** Si l'un de ces faits apparaît, signaler dans la conversation **avant** tout changement de stratégie, expliquer le risque, les preuves, les options, les conséquences et la recommandation, puis confirmer le choix humain avant de changer l'orientation :

1. Un prototype P1–P3 ne peut pas rester strictement jetable/isolé ou requiert de lire/modifier le profil existant, une SQLite historique, un backup, un marqueur réel, une migration 007 ou d'exposer un nouvel IPC writer.
2. Une preuve CI/adversariale R4–R9 révèle une faille de corruption, d'écriture concurrente, d'intégrité ou de provenance dont le risque ne peut pas être contenu dans les fixtures.
3. Le couplage technique Rust/Tauri/SQLite v7/React rend la piste produit impossible ou beaucoup plus coûteuse que prévu ; la portée P1/P2 doit changer matériellement.
4. L'utilisateur change ses priorités ou demande une exploitation opérateur réelle, distribution, Windows Hello, récupération d'historiques ou bascule v7.
5. Les critères de M3.2 ou les STOP de gouvernance changent effectivement après un examen formel du dépôt et d'une nouvelle décision utilisateur.

Proposer alors soit le **maintien** de PRODUCT_FIRST_PARALLEL_SAFETY, soit une priorité temporaire à un gate précis, soit une autre voie, avec impact sur le parcours utilisateur et la sécurité. À défaut de déclencheur, **conserver ce choix d'une conversation à l'autre sans redemander inutilement**.

## STOP inchangés et preuve de gouvernance

`M3.2=IN_PROGRESS_NOT_ACCEPTED`; writer/R1–R9 de production `NOT_PROVEN`; G2B `NOT_ACCEPTED`; G2C `NOT_AUTHORIZED`; G3 réel `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`; prospective `NOT_STARTED`; D3b-4/5 STOP ; PR #35 et #215 DRAFT, ne pas fusionner telles quelles. Aucune donnée v6/v7 opérateur, profil Greenfield existant, journaux, sauvegardes, ACL, migration 007, code runtime writer/IPC, Windows Hello natif, marqueur persistant, recovery ou activation sans gate supplémentaire.

Pour chaque PR : re-fetch `main`, PR/issues, Windows CI SHA exact et logs ; audits diff/reviews/threads ; ruleset **Protect main** ACTIVE strict bypass=[] ; squash avec `expected_head_sha`, CI postmain indépendante, issue #38 **append-only** ; actualiser les deux prompts et les handoffs MD/JSON ainsi que STATE/NEXT/gates et les deux roadmaps. Ce document reste l'autorité de la **priorité**, pas du passage de gate. Dernier état GitHub prime sur les anciens SHA et annotations « non qualifiée » des checkpoints historiques.
