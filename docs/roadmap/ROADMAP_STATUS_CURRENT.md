# Fabulaxiom — suivi de la roadmap V1 (état actualisé au 21 octobre 2026)

**Référence de suivi, non autorisation d'exécution.** Établi après re-fetch GitHub de `main=e35b7c92441c517d4f0fcacb829711c4d1e9da97`, [PR #96](https://github.com/LaurentCOLL1/Fabulaxiom/pull/96) fusionnée, CI exact-head #39414915855 SUCCESS (73 étapes) et CI push main #39416303498 SUCCESS (72 étapes). Toujours re-fetch avant de prendre une décision ultérieure.

Les [cinq plans de source](README.md) gardent leurs exigences et preuves historiques. Le présent statut **ne transforme pas** un test synthétique en fonctionnalité livrée, ni un jalon futur en autorisation.

## 21 octobre 2026 — état après PR #100 fusionnée

GitHub vérifié : PR [#100](https://github.com/LaurentCOLL1/Fabulaxiom/pull/100) MERGED, `main=bf59b28b437470a4759a5971968e8f00f9fa895c`, head PR `95e2e0385979e2b226aa1d6289e12250c6e6e19d`, CI PR #39533766395 SUCCESS et CI main #39534698504 SUCCESS, terminales sur leurs SHA respectifs. Aucun nouveau commit ne peut réutiliser ces CI. Preview des chemins qui créeraient un cycle, blocage des corrections avant révocation humaine, 32 Vitest et 36 Chromium : **uniquement un atelier sur données fictives**, ni produit accepté ni preuve Windows.

M3.1 COMPLETE/MERGED/NORMALIZED ; **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT. Étape produit suivante : UX des trois ordres monde/narration/révélation sur fixtures sans persistance et tests neufs. G2A PASS metadata-only, accord consommé ; écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucun original v6/v7, journaux/sidecars, sauvegardes, ACL, marqueur, migration007, writer IPC, M3.3, ComfyUI ou release. Nouveau script Windows uniquement avec texte intégral/effets/interactions et accord explicite.

---

## 21 octobre 2026 — candidat de couverture multiromans M3.2 (non accepté)

Sur le **seul atelier navigateur entièrement inventé**, une deuxième scène du même Univers est placée dans un autre roman ; chaque scène possède ses révisions immuables propres. Quatre tests unitaires (36 total) et deux Chromium (38 total) sont **proposés, CI nouvelle encore requise**. Aucune chronologie du monde ni ordre de révélation n'est déduit des positions relatives des manuscrits. Cette preuve fictive ne remplace pas le CRUD persistant, l'essai Windows ni la normalisation M3.2. PR #35 reste DRAFT, G2B–G6 STOP.

## Matrice de conformité

| Jalon | État réel connu | Conformité / prochaine preuve |
| --- | --- | --- |
| M0 — architecture et outillage | **COMPLETE + MERGED + NORMALIZED** | Architecture Windows Tauri 2 / React / Rust, CI et Ollama en lecture de statut qualifiés ; aucune fonctionnalité M4+ implicite |
| M1 — persistance et hiérarchie | **COMPLETE + MERGED + NORMALIZED** (M1.1–M1.5) | SQLite, scènes/révisions et backup/restore acceptés selon [plan M1](M1_PERSISTENCE_PROJECT_FOUNDATION.md), les données historiques restent protégées |
| M2 — entités, faits, revue | **COMPLETE + MERGED + NORMALIZED** (M2.1–M2.5) | Dernière normalisation PR #30 ; faits avec provenance et statut humain selon [plan M2](M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md) |
| M3.1 — fondation temporelle v7 | **COMPLETE + MERGED + NORMALIZED**, uniquement dans le périmètre accepté | PR #33 implémentation fusionnée (merge `922d155d4f4321ed8b90955d4ea96388751f0daf`) ; PR #34 normalisation fusionnée (`f7eabfea74480d307b52d4b053730021efc95352`). **Aucune migration automatique 007 vers la production v6** ; v7 isolée et read-only uniquement selon preuves antérieures |
| M3.2 — chronologie manuelle | **IN_PROGRESS_NOT_ACCEPTED** | PR #35 ouverte en brouillon ; code, projections et tests fictifs, G2/G3 de provenance et concurrence. **Manquent** les CRUD manuels et la GUI opérateur qualifiés sur la base acceptée, le contrôle réel de préservation des données, la CI du PR final et une normalisation distincte. Ne pas utiliser le nombre de PR/toys comme preuve d'acceptation produit |
| M3.3 — relations directionnelles | **NOT_STARTED_NOT_AUTHORIZED** | Reste après M3.2 normalisée |
| M3.4 — connaissances et croyances | **NOT_STARTED_NOT_AUTHORIZED** | Reste après M3.3 |
| M3.5 — narrateur / exposition lecteur | **NOT_STARTED_NOT_AUTHORIZED** | Reste après M3.4 |
| M3.6 — états narratifs évolutifs | **NOT_STARTED_NOT_AUTHORIZED** | Reste après M3.5 ; M3 global non terminé |
| M4 — recherche et mémoire | **NOT_STARTED_NOT_AUTHORIZED** | FTS5, embeddings et récupération contextuelle restent hors périmètre M3 |
| M5 — intégration Ollama complète | **NOT_STARTED_NOT_AUTHORIZED** | Le simple statut Ollama M0 ne livre pas M5 (génération, queue, streaming, validation) |
| M6 — cohérence | **NOT_STARTED_NOT_AUTHORIZED** | Pas de moteur accepté de contradictions |
| M7 — assistance à l'écriture | **NOT_STARTED_NOT_AUTHORIZED** | Les éditeurs manuels M1/M2 ne livrent pas les fonctions IA de M7 |
| M8 — gestion narrative avancée | **NOT_STARTED_NOT_AUTHORIZED** | Pas de carte des relations / retcon et tableaux de bord acceptés |
| M9 — imports, exports, résilience, distribution | **NOT_STARTED_NOT_AUTHORIZED** | Les sauvegardes M1.5 n'équivalent pas à l'ensemble M9 ni à une release |
| Références visuelles / ComfyUI | **PROPOSAL_ONLY_NOT_AUTHORIZED** | [Proposition](V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md) et issue [#19](https://github.com/LaurentCOLL1/Fabulaxiom/issues/19) ouverte ; pas de code ComfyUI, pas de garantie de sauvegarde des images |

## 20 octobre 2026 — nouveau jalon candidat, actions humaines sur fixtures

Une nouvelle tranche `feat/m3-2-fictional-manual-chronology-lab-20261020` propose, sans livraison de production, un [laboratoire navigateur fictif](../qualification/M3_2_SYNTHETIC_MANUAL_CHRONOLOGY_LAB.md) : créer une date, saisir `A avant B`, rejeter les cycles, corriger par supersession et révoquer avec historique. Treize tests frontend doivent être vérifiés au HEAD de la nouvelle PR. **Cette démonstration n'est pas le CRUD persistant ni l'acceptation Windows** exigés ; M3.2 demeure `IN_PROGRESS_NOT_ACCEPTED`. PR #35 et gates G2B–G6 inchangés.

## 20 octobre 2026 — scène/révision historique explicite (nouvelle tranche sur fixtures)

PR #98 a été fusionnée avec CI source-only, 13 tests Vitest et 32 cas Chromium, sur `main=7477001cd0ebc69d4701f21eddbda898f94c79c5`. La [tranche suivante](../qualification/M3_2_FICTIONAL_SCENE_REVISION_EXACT_BINDING.md) ajoute un choix manuel de `scene_id` et `revision_id` immuable **inventés**, y compris une version historique, avec rejets déterministes des références étrangères et préservation de l'ancien lien par supersession. 22 cas Vitest/34 cas Chromium prévus ; CI sur le nouveau commit non encore acquise à la rédaction. **Pas de CRUD persisté ni de certification opérateur ; M3.2 IN_PROGRESS_NOT_ACCEPTED.**

## 21 octobre 2026 — historique du candidat PR #100, depuis fusionné

PR #99 fusionnée à `main=205a328150c90bf1fb4f52abd7fb8c04f3959468`, CI PR #39480662913 SUCCESS et post-merge #39482419125 SUCCESS. Candidat [prévisualisation de conflit et correction](../qualification/M3_2_FICTIONAL_CONFLICT_WITNESS_AND_CORRECTION_PREFLIGHT.md) : afficher les relations humaines exactes constituant un chemin cyclique avant tout ajout ; nommer les liens bloquant une correction sans les retirer automatiquement, préserver la révision de scène historique. Le laboratoire navigateur source-only reste **non persistant** ; 32 tests Vitest et 36 interactions Chromium proposés, nouvelle CI obligatoire. **M3.2 IN_PROGRESS_NOT_ACCEPTED**, aucune promotion G2B–G6.

## Écart principal et chemin de retour au produit M3.2

Le [plan M3](M3_TIME_KNOWLEDGE_RELATIONSHIPS.md) prévoit précisément **saisie/édition manuelles des ancres temporelles et contraintes avant/après**, dates exactes/approximatives/relatives/inconnues, deux Universes, plusieurs romans, références de scènes et révisions immuables, refus des cycles et conflits, distinction visible entre **ordre du monde**, **ordre de narration** et **ordre de révélation**, fonctionnement hors ligne, puis **tests Windows réels**, preuves de sauvegarde/activation intactes, CI au SHA exact, fusion et normalisation indépendante.

Les tranches M3.2 déjà fusionnées (jusqu'à #100) qualifient principalement des **contre-exemples et protections sur des fichiers publics et fixtures SQLite fictives**. Elles sont utiles pour empêcher une corruption ou une conclusion de sécurité erronée, mais **n'achèvent pas les livrables M3.2** et ne doivent pas devenir une boucle indéfinie d'audits sans objectifs fonctionnels.

La voie productive suivante : continuer en parallèle *seulement sur jeux de données inventés* les scénarios de CRUD/chronologie UI prévus, avec traçabilité exigences→tests, tout en conservant une **barrière indépendante** avant tout accès réel Windows. Les sources de production v6, v7 isolée, sauvegardes, journaux, ACL et marqueurs ne doivent pas être ouvertes ou migrées implicitement.

### Décision actuelle des gates (séparée de la livraison produit)

- G2-A : `PASS_METADATA_ONLY_OWNER_REPORTED` après une seule observation Windows expressément autorisée ; permission consommée.
- `PROCESS_WRITER_ABSENCE=NOT_PROVEN` ; identités réelles et chaîne de confiance non établies par des tests synthétiques.
- G2-B/C/D et G3–G6 : **NOT_AUTHORIZED** ; vrai G3 `STOP_UNAVAILABLE`.
- Provenance historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; baseline prospective `NOT_STARTED` ; issues #36 et #38 ouvertes, PR #35 en brouillon.
- Ne pas lancer migration 007 en production, writer IPC, PR #35 merge, M3.3, ComfyUI ou release. Toute commande Windows exige texte intégral, effets, conditions STOP et **nouvelle autorisation spécifique**.

## Discipline de suivi de la roadmap

1. Le statut d'une sous-étape est fondé sur preuve acceptée **et** normalisation, pas sur un nombre de tests ou un prototype fonctionnel.
2. Vérifier la conformité des exigences par identifiants Mx.y et tests datés, distinguer explicitement « synthetic-only », « implementation merged », « operator accepted », « normalized ».
3. Réviser ce fichier **à chaque clôture de subdivision ou changement effectif de périmètre**, avec `docs/continuity/HANDOFF_CURRENT.md` et `HANDOFF_CURRENT.json` dans la même PR.
4. Aucun jalon suivant ne peut être déclaré autorisé par un changement de texte, un badge de CI ou un accord antérieur destiné à une autre opération.
5. Tous les en-têtes « en attente » d'anciennes PR dans les plans détaillés sont des **preuves historiques datées** ; ce tableau résume la dernière vérification GitHub du présent checkpoint.

**Sources d'autorité :** [roadmap V1](FABULAXIOM_ROADMAP_V1.md), [M1](M1_PERSISTENCE_PROJECT_FOUNDATION.md), [M2](M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md), [M3](M3_TIME_KNOWLEDGE_RELATIONSHIPS.md), [ComfyUI proposition](V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md), [gates actuels](../continuity/M3_2_GATE_DECISION_CURRENT.md).
