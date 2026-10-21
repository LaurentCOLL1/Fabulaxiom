# Fabulaxiom — suivi de la roadmap V1 (état actualisé au 21 octobre 2026)

**21 octobre 2026 — PR #117 fusionnée et CI post-fusion exacte confirmée :** source `99d78a46e61a0765b6673353900cea55eb039e74`, CI #39653506345 **SUCCESS** (74 étapes, 112 tests Rust, 44 tests de continuité, 21 tests d'inventaire, 50 Chromium par mode). Fusion protégée `main=b76e6c00c579bee36c194872e3679c48fe9788fa` ; CI post-merge #39655214998 **SUCCESS terminale** sur ce SHA. La règle permanente de parallélisation des tâches indépendantes est toujours en vigueur.

**Troisième tranche test-only candidate :** reprise strictement limitée de la reformulation humaine explicite d'une précédence révoquée (`restate_revoked_precedence`) et du SQL candidat `m3_2_active_precedence_candidate.sql` sur SQLite **uniquement en mémoire**. Cinq tests Rust supplémentaires prévus : source révoquée obligatoire, interdiction de cycle, unicité, conservation immuable et blocage d'ancres retirées / insertion brute abusive. Le module reste `#[cfg(test)]`, sans exposition Tauri, migration 007 ni donnée locale opérateur. Révocation des reformulations, successeurs et corrections en chaîne sont hors portée. CI nouvelle au HEAD exact requise.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT/non fusionnable ; absence d'écrivain SQLite réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, provenance `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune commande Windows opérateur, base v6 active/v7 isolée, sidecars, ACL, sauvegardes, activation marker, IPC writer, M3.3, ComfyUI ou release.


**21 octobre 2026 — PR #116 fusionnée et CI post-fusion vérifiée :** HEAD source `0b2555833c1a2c0152cba2185c8122f3d3ecbbae`, CI PR #39626827246 **SUCCESS** (74 étapes Windows ; 106 Rust dont 6 nouveaux tests RAM, 42 contrats de continuité, 21 inventaires SQLite, 50 Chromium par mode). Fusion protégée `main=388cb745888f9f2d4d0a07fce1ed19fad9b4a548`, CI post-merge #39628479487 **SUCCESS terminale au SHA exact**. PR #35 reste DRAFT/non fusionnable. Règle permanente de parallélisation inchangée.

**Deuxième tranche source-only candidate :** reprise bornée de `decide_anchor`, `decide_precedence`, `supersede_anchor_atomically`, `list_current_anchor_ids`, `list_current_precedence_ids`, `list_anchor_decisions` et de `m3_2_chronology_decisions_candidate.sql` historique. Module Rust `#[cfg(test)]` uniquement, SQL candidat chargé **après v6 et v7 fictifs en mémoire** ; six nouveaux tests Rust prévus pour révocation, conservation de l'historique, rollback transactionnel, Univers distincts, cycles/contraintes. Aucune migration 007, aucun IPC ni base réelle ; CI au HEAD candidat obligatoire. Les restatements et chaînes de corrections restent hors portée.

**STOP maintenu :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; `PROCESS_WRITER_ABSENCE=NOT_PROVEN`; G2-B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Aucune action opérateur Windows, SQLite active v6, isolée v7, sauvegarde, ACL, sidecar, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release.


**21 octobre 2026 — correction de qualification PR #116 :** la première CI #39625498131 a délibérément **échoué** au contrôle d'inventaire textuel des occurrences Rust SQLite après ajout du module `#[cfg(test)]`. Comptage exact observé dans le nouveau fichier : `Connection::open_in_memory` **1**, `run_migrations` **1**, et **0** occurrence pour `Connection::open` disque, ouverture applicative, ATTACH, VACUUM, flags ouverts ou API backup brute. Après revue limitée à ces textes publics, l'inventaire attendu ajoute explicitement `(1,0,1,0,0,0,0)` pour `src-tauri/src/m32_manual_chronology.rs`, conserve toutes les entrées existantes et ajoute trois tests adversariaux (21 au lieu de 18). Toute autre occurrence, y compris dans ce module, reste un **STOP**. Cette qualification ne prouve pas l'absence de writer réel ni la sécurité des fichiers opérateur ; une nouvelle CI complète au nouveau HEAD est obligatoire.


**21 octobre 2026 — PR #115 fusionnée :** HEAD source `3f1c5676f7035398b61bc143a16eae5e115cdfbe`, CI PR #39619267259 **SUCCESS** (74 étapes, 40 tests de continuité, 60 Vitest fictifs, 50 Chromium par mode, 100 tests Rust au commit source). Fusion protégée `main=33846c8c6813acda5eda5089827f81df99175d2c` ; CI post-fusion #39620942276 **SUCCESS terminale au SHA exact**. La règle de parallélisation reste active. La PR #35 demeure OPEN/DRAFT non fusionnable ; le portage décrit ci-dessous est indépendant, strictement test-only, et ne constitue aucune autorisation de fusion de #35.

**Nouvelle tranche candidate source-only :** portage limité des opérations `create_calendar`, `create_anchor`, `create_precedence`, `list_anchors`, `list_precedences` du Rust historique de PR #35 vers un module `#[cfg(test)]` sur `main`, avec six tests utilisant exclusivement des bases SQLite **en mémoire**, les deux Univers fictifs, quatre temporalités, ordre humain explicite, cycles interdits et révisions immuables. **Aucun IPC**, pas d'activation du schéma v7 réel ou de migration 007, aucune ouverture des fichiers opérateur. Une nouvelle CI SHA exact doit encore qualifier cette tranche ; les fonctions de supersession de PR #35 ne sont pas portées dans cette étape.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, réel writer `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, historique 21/3/2 non résolu, baseline prospective `NOT_STARTED`, aucune opération Windows opérateur ni production v6, v7 isolée, backups, ACL, journaux, activation marker, migration 007, writer IPC, M3.3 ou release.


**21 octobre 2026 — PR #114 fusionnée et CI post-fusion vérifiée :** la [PR #114](https://github.com/LaurentCOLL1/Fabulaxiom/pull/114), source `8262659d58045c127fe4ee3ac56e6dd5681a9f5f` et [CI PR #39612803528](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39612803528) **SUCCESS (job Windows 74 étapes)**, a été fusionnée sous protection à `main=ddb23311f40f09c04983b164ccd7afa361698ea8`. La [CI main #39614175650](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39614175650) est **SUCCESS terminale** au SHA de fusion exact. La règle permanente de parallélisation des tâches indépendantes figure dans `HANDOFF_PROTOCOL.md` sur `main`, sans autoriser les opérations Windows privées.

**Décision inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; PR #35 OPEN/DRAFT, GitHub `mergeable=false` au HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` et prospective `NOT_STARTED` ; absence d'écrivain réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucune migration 007, writer IPC, M3.3, release ni opération sur production v6/isolée v7, sauvegardes, ACL, sidecars, marqueurs ou Windows opérateur.

**Voies parallèles sûres à poursuivre :** A : réconciliation *source-only* de la PR #35, sur branche nouvelle et fixtures inventées ; B : étude documentaire des cinq témoins historiques (issue #36), sans falsifier la provenance ; C : examen du protocole de baseline prospective et du propriétaire SQLite non migrant (issue #38), sans lecture de sources privées. Ces études peuvent avancer en parallèle ; commits concurrents vers la même branche et merges restent séquentiels, avec re-fetch et CI exacte. [Plan borné de réconciliation](../qualification/M3_2_PR35_SAFE_RECONCILIATION_PLAN.md).


**Checkpoint GitHub confirmé le 21 octobre 2026 :** PR [#113](https://github.com/LaurentCOLL1/Fabulaxiom/pull/113) **MERGED** sous Protect main, HEAD source `6fd369de970e6e35d42c2162f197eb57009a1d42`, [CI exacte #39605681206](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39605681206) **SUCCESS** (74 étapes Windows, 60 Vitest atelier fictif, 50 Chromium par mode), `main=e74f1001c01eff1f37c8b35d97d4ef34f6fbccb3` et [CI post-fusion #39607280677](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39607280677) **SUCCESS terminale au SHA exact**. PR #35 reste OPEN/DRAFT, GitHub `mergeable=false` ; source réelle G2B–G6 non autorisée, absence d'écrivain SQLite réel `NOT_PROVEN`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`. Aucun geste opérateur local réalisé.

**Organisation de la roadmap :** mener en parallèle, quand ils sont indépendants, les travaux source-only sur fixtures, la traçabilité des exigences et la recherche documentaire des preuves #36 / de la baseline #38. Ne pas fusionner plusieurs branches concurrentes vers `main` sans re-fetch, CI et décision séquentielle ; aucune promotion M3.2 ni G2–G6. Voir [protocole](../continuity/HANDOFF_PROTOCOL.md).


**21 octobre 2026 — résultat terminal post-fusion PR #112 :** la CI push [#39597532619](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39597532619) a terminé **SUCCESS** sur `main=3c489aa727129e4b090e2e80a49a93fb3fa95877`, SHA exact du merge #112. Les mentions plus anciennes « en cours au checkpoint » sont des photographies historiques, et ne décrivent pas l'état terminal. Cette mise à jour de la PR #113 impose une CI nouvelle sur son nouveau HEAD. M3.2 reste IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, writer réel NOT_PROVEN, G2B–G6 STOP, aucun essai Windows opérateur ni SQLite protégée.


**21 octobre 2026 — PR #112 fusionnée avec CI source exacte :** [PR #112](https://github.com/LaurentCOLL1/Fabulaxiom/pull/112) MERGED sous Protect main au SHA `3c489aa727129e4b090e2e80a49a93fb3fa95877` ; HEAD source `56c5d4d55a616469cda36c5fef7f63369a08bdb2`, [CI #39596187154](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39596187154) terminale **SUCCESS** au HEAD exact (74 étapes Windows, 60 Vitest d'atelier fictif, 50 Chromium par mode normal et CSP stricte). [CI push `main` #39597532619](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39597532619) **EN COURS AU CHECKPOINT** au SHA de fusion ; revérification terminale requise. Cette fonctionnalité fictive relie deux révisions immuables explicitement choisies à une chaîne de précédences humaines actives sans faire dépendre le temps du monde de l'ordre narratif.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT, G2-A metadata-only (accord ponctuel consommé), écrivain SQLite réel `NOT_PROVEN`, G2-B à G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucun Windows opérateur, base réelle v6/v7, sauvegarde, ACL, WAL/SHM, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release.


**Candidat de preuves du monde par révisions exactes — 21/10/2026 :** le laboratoire fictif permet de sélectionner deux scènes et leurs révisions immuables pour lire une chaîne de précédences **humaines actives** entre leurs ancres, lorsque chacune possède exactement une ancre courante. Dates, ordre narratif entre romans et révélations ne sont pas déduits. Historique/révisions étrangères/ambiguïté : refus ou indétermination. 60 Vitest et 50 Chromium par mode **à qualifier sur une nouvelle CI**. Aucune intégration `App.tsx`/Tauri/SQLite.

**STOP :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, G2-A accord consommé, écrivain réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE. Aucun Windows opérateur, original SQLite v6/v7, sauvegarde/ACL/journal, migration 007, IPC writer, M3.3 ou release.


**Vérification terminale post-fusion #110 (21 octobre 2026) :** [CI `main` #39591429432](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39591429432) **SUCCESS terminale** sur le SHA exact `2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b` ; PR #110 MERGED. Les anciennes mentions « en cours » documentent uniquement un instantané antérieur. Cette normalisation dans la PR #111 nécessite sa **propre CI fraîche au HEAD modifié** ; les deux CI de #110 ne sont pas transférables. **M3.2 toujours IN_PROGRESS_NOT_ACCEPTED**, PR #35 DRAFT ; G2-A métadonnées avec accord consommé, absence d'écrivain réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE ; aucune commande Windows opérateur, originale SQLite, migration 007, IPC writer, M3.3 ni release.


**Checkpoint GitHub confirmé le 21 octobre 2026 :** PR [#110](https://github.com/LaurentCOLL1/Fabulaxiom/pull/110) **MERGED** sous Protect main sur `main=2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b` ; source `f69e36a24aedda15222bb3a4e3a198ba57d0174a`, CI PR [#39577527093](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39577527093) **SUCCESS terminale sur ce HEAD** (74 étapes Windows, 55 Vitest d'atelier fictif et 48 Chromium par mode normal / précompilé strict CSP). CI push [#39591429432](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39591429432) **EN COURS AU CHECKPOINT** sur le SHA du merge : re-fetch terminal obligatoire. Les anciennes mentions « candidat » sont historiques ; aucune CI d'ancien SHA transférable.

**Sécurité inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT ; G2-A PASS sur métadonnées seulement (accord unique consommé), absence d'écrivain SQLite réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`. Aucune commande Windows opérateur, aucun original v6/v7, sauvegarde, WAL/SHM, ACL, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release.

---


**21 octobre 2026 — candidat de produit M3.2, données fictives uniquement :** effet d'une révocation de lien temporel explicitement déclaré, aperçu de la preuve restante (ou ordre indéterminé) avant confirmation humaine. Réutilise uniquement le moteur actuel, sans nouvelle date ni suppression automatique. Cibles CI neuve : 55 Vitest atelier et 48 Chromium par mode. Ne remplace ni CRUD SQLite ni essai opérateur Windows ; G2B–G6 STOP.


**Checkpoint terminal vérifié le 21 octobre 2026 :** PR #108 fusionnée sur `main=ba4b8a599910cef6d1c76fa1e4fb561a0b45e631`, CI source #39572172593 SUCCESS (51 Vitest, 46 Chromium par mode), CI push post-fusion [#39573518324](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39573518324) **SUCCESS** au SHA exact. Mentions « en cours » ci-dessous historiques. M3.2 NON ACCEPTÉE, PR #35 DRAFT, écrivain réel NOT_PROVEN, G2B–G6 STOP. Aucune exécution opérateur ni mutation SQLite.


**Checkpoint public du 21 octobre 2026 :** PR [#108](https://github.com/LaurentCOLL1/Fabulaxiom/pull/108) MERGED sur `main=ba4b8a599910cef6d1c76fa1e4fb561a0b45e631`, CI exacte de PR #39572172593 SUCCESS (74 étapes Windows, 51 tests atelier, 46 Chromium dans deux modes). CI post-fusion #39573518324 **EN COURS au présent instantané**, résultat terminal à vérifier. Fonctionnalité exclusivement fictive de refus des anciennes sélections historiques ; M3.2 NON ACCEPTÉE, PR #35 DRAFT, G2B–G6 STOP, écrivain SQLite réel NOT_PROVEN.


**Tranche candidate M3.2 du 21 octobre 2026 (non acceptée) :** UX fictive de sélection d'ancre devenue historique après supersession : avertissement lisible, option historique désactivée, aucune relation actuelle tirée de cet ID ; isolement des choix entre Univers. Cibles 51 tests atelier/46 Chromium par mode, CI au nouveau SHA nécessaire. Le vrai CRUD/acceptation Windows et les gates G2B–G6 restent fermés.


**Vérification terminale (21 octobre 2026) :** la CI push main [#39567933461](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39567933461) après fusion protégée PR #106 est maintenant **SUCCESS** au `main=fbfc785afa6e5bdf92c337004d1bd2f925c4957a`. La CI PR #39566947725 avait déjà terminé SUCCESS (48 tests atelier, 44 Chromium par mode). Les anciens « en cours » sont des preuves historiques datées ; aucun nouveau gate ouvert : M3.2 NOT_ACCEPTED, G2B–G6 STOP, écrivain réel NOT_PROVEN. La présente PR documentaire demande une CI neuve au HEAD exact.


**Checkpoint GitHub 21 octobre 2026 :** [PR #106](https://github.com/LaurentCOLL1/Fabulaxiom/pull/106) fusionnée au `main=fbfc785afa6e5bdf92c337004d1bd2f925c4957a`. CI PR #39566947725 terminale SUCCESS (48 tests atelier / 44 Chromium dans les deux modes, 74 étapes Windows), CI push main #39567933461 **EN COURS au checkpoint**. Laboratoire fictif de preuve humaine uniquement ; aucun original SQLite/Windows, M3.2 non acceptée, PR #35 DRAFT, G2B–G6 STOP.


**Vérification terminale du 21 octobre 2026 :** CI push `main=997b60901e1f18a426eae3efa34ddb29c07b5721` [#39554622761](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39554622761) désormais **SUCCESS** au SHA exact, après PR #104 MERGED (CI PR #39553745685 SUCCESS, 42 Vitest atelier / 41 Chromium). Les mentions antérieures « en cours » sont des instantanés historiques. M3.2 non acceptée, G2-B–G6 STOP, writer absence NOT_PROVEN. Aucun test Windows opérateur.


**Référence de suivi, non autorisation d'exécution.** Établi après re-fetch GitHub de `main=e35b7c92441c517d4f0fcacb829711c4d1e9da97`, [PR #96](https://github.com/LaurentCOLL1/Fabulaxiom/pull/96) fusionnée, CI exact-head #39414915855 SUCCESS (73 étapes) et CI push main #39416303498 SUCCESS (72 étapes). Toujours re-fetch avant de prendre une décision ultérieure.

Les [cinq plans de source](README.md) gardent leurs exigences et preuves historiques. Le présent statut **ne transforme pas** un test synthétique en fonctionnalité livrée, ni un jalon futur en autorisation.

## 21 octobre 2026 — état après PR #100 fusionnée

GitHub vérifié : PR [#100](https://github.com/LaurentCOLL1/Fabulaxiom/pull/100) MERGED, `main=bf59b28b437470a4759a5971968e8f00f9fa895c`, head PR `95e2e0385979e2b226aa1d6289e12250c6e6e19d`, CI PR #39533766395 SUCCESS et CI main #39534698504 SUCCESS, terminales sur leurs SHA respectifs. Aucun nouveau commit ne peut réutiliser ces CI. Preview des chemins qui créeraient un cycle, blocage des corrections avant révocation humaine, 32 Vitest et 36 Chromium : **uniquement un atelier sur données fictives**, ni produit accepté ni preuve Windows.

M3.1 COMPLETE/MERGED/NORMALIZED ; **M3.2 IN_PROGRESS_NOT_ACCEPTED**, PR #35 OPEN/DRAFT. Étape produit suivante : UX des trois ordres monde/narration/révélation sur fixtures sans persistance et tests neufs. G2A PASS metadata-only, accord consommé ; écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucun original v6/v7, journaux/sidecars, sauvegardes, ACL, marqueur, migration007, writer IPC, M3.3, ComfyUI ou release. Nouveau script Windows uniquement avec texte intégral/effets/interactions et accord explicite.

---

## 21 octobre 2026 — checkpoint historique du candidat PR #102, depuis fusionné

Sur le **seul atelier navigateur entièrement inventé**, une deuxième scène du même Univers est placée dans un autre roman ; chaque scène possède ses révisions immuables propres. Quatre tests unitaires (36 total) et deux Chromium (38 total) sont **proposés, CI nouvelle encore requise**. Aucune chronologie du monde ni ordre de révélation n'est déduit des positions relatives des manuscrits. Cette preuve fictive ne remplace pas le CRUD persistant, l'essai Windows ni la normalisation M3.2. PR #35 reste DRAFT, G2B–G6 STOP.

## 21 octobre 2026 — clôture technique fictive de PR #102, pas acceptation M3.2

PR [#102](https://github.com/LaurentCOLL1/Fabulaxiom/pull/102) **fusionnée** sur `main=1f0a8cd9a369106202b57102aa28915de65b7472`, après CI PR [#39543328344](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39543328344) SUCCESS au HEAD `07baf294286d427185c0817310d82418eb8c3fd2` (36 tests Vitest atelier, 38 scénarios Chromium en deux modes), et push main [#39544279201](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39544279201) SUCCESS au merge exact. Couverture de deux romans dans un même Univers inventé, révisions de scènes filtrées strictement. **Ne pas confondre position manuscrit, précédences humaines et révélation lecteur**. Les mentions « CI à qualifier » des sections précédentes sont des checkpoints antérieurs, pas le statut actuel. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 DRAFT, G2B–G6 STOP, aucun vrai SQLite/Windows ; M3.3 et release non autorisées.

## 21 octobre 2026 — historique du candidat PR #104, depuis fusionné

Une nouvelle interaction dans l'atelier de chronologie fictif sélectionne deux scènes par identifiants, compare **uniquement** leurs positions dans un même roman (ou affiche l'indétermination pour deux romans), conserve « chronologie du monde indéterminée » et « révélation au lecteur non renseignée ». Six tests Vitest et trois Chromium proposés : **42 tests atelier / 41 scénarios Chromium à qualifier sur un nouveau SHA**. Cela ne livre ni calendrier canonique, ni ordre global, ni GUI native acceptée. G2B–G6 et PR #35 inchangés.

## 21 octobre 2026 — après fusion protégée PR #104 (seul laboratoire fictif)

PR [#104](https://github.com/LaurentCOLL1/Fabulaxiom/pull/104) MERGED sur `main=997b60901e1f18a426eae3efa34ddb29c07b5721` ; source HEAD `b320b711763659d9a3af670b685254eeb8b815e9`, CI PR #39553745685 SUCCESS (42 Vitest atelier, 41/41 Chromium dans les modes normal et précompilé strict CSP, 74 étapes Windows). CI push main #39554622761 encore **EN COURS** au moment de cet instantané. Le comparateur de trois ordres ne compare des scènes qu'au sein d'un même roman ; **monde et révélation restent indéterminés**. Pas de saisie de connaissances ou révélations M3.4/M3.5, ni nouvelle persistance, ni App.tsx ou Tauri. Les anciens candidats en dessous sont historiques. **M3.2 = IN_PROGRESS_NOT_ACCEPTED** ; G2-B à G6 fermés, PR #35 DRAFT, M3.3 non autorisée.

## 21 octobre 2026 — historique du candidat PR #106, depuis fusionné

Intégration **proposée, non qualifiée** du module existant `M32WorldOrderComparison` dans l'atelier manuel fictif, avec consultation de deux ancres, témoins déterministes et motif humain, exclusion des liens révoqués, et actualisation sans écriture après révocation explicite. Objectifs : **48 tests Vitest atelier / 44 scénarios Chromium par mode**, nouvelle CI à prouver. Aucune inférence du temps du monde depuis la narration ni de révélation lecteur, pas de Tauri/App.tsx/SQLite original. M3.2 IN_PROGRESS_NOT_ACCEPTED, G2B–G6 STOP.

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
