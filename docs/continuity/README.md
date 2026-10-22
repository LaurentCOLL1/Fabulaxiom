# Fabulaxiom — Point d'entrée pour reprendre les discussions ChatGPT

**22 octobre 2026 — PR #122 MERGED sous Protect main :** HEAD exact source `1ade25c7b8c500d712c452a08d90ed26a1ffbe89`, [CI #39717330885](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39717330885) **SUCCESS terminale**, 74 étapes Windows, 128 Rust, 53 contrôles de continuité. Fusion protégée `main=52b06099ba0cff0da15fa697b0e2043afc883a00`, CI post-main [#39718851557](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39718851557) **SUCCESS terminale au SHA exact**, à re-fetch au SHA exact. Sixième tranche: révocation immuable du seul successeur (SQL candidat, `revoke_successor`, `list_successor_history`), uniquement Rust `#[cfg(test)]` et SQLite fictive RAM, historique préservé. Aucune correction récursive.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence de writer SQLite réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. PR #35 OPEN/DRAFT ; aucune commande Windows opérateur, original SQLite v6/v7, backups/ACL/sidecars/marker, migration 007, writer IPC, M3.3, ComfyUI ni release. La règle permanente de parallélisation des lectures/analyses et sérialisation des écritures/fusions demeure.

**Prochain travail source-only possible :** après cette normalisation et CI HEAD exact, analyser et éventuellement développer **séparément** la correction récursive à partir de la PR #35 historique (`m3_2_recursive_chain_candidate.sql`) sur une nouvelle branche avec SQLite uniquement en RAM et tests adversariaux ; jamais de promotion des gates réels.


**22 octobre 2026 — PR #121 MERGED sous Protect main :** HEAD source `6a1a22dedaa4e3d2c302a56959083017578dc7da`, CI PR [#39713440057](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39713440057) **SUCCESS terminale** (74 étapes Windows, 125 tests Rust). Fusion protégée `main=08caad24e20eae484e94fd084edb487b5c370bd5`; CI post-fusion [#39716352685](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39716352685) **SUCCESS au SHA exact**.

**Tranche suivante candidate, non qualifiée :** sixième importation Rust limitée à une révocation terminale immuable d'un successeur fictif : `m3_2_successor_revocations_candidate.sql`, `revoke_successor`, `list_successor_history`, 3 nouveaux tests adversariaux. Module `#[cfg(test)]` et SQLite exclusivement `Connection::open_in_memory()`. Ne pas confondre cette tranche avec les chaînes récursives de PR #35 ; aucune migration de production ou commande Tauri.

**STOP non levé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; absence d'écrivain SQLite réel `NOT_PROVEN` ; G2B–G6 `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED`. Pas de commande Windows sans approbation distincte, aucune SQLite réelle v6/v7, sauvegarde, ACL, sidecar, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release. Travailler en parallèle uniquement sur les sources et analyses indépendantes ; intégrations et fusions séquentielles avec re-fetch/CI au HEAD exact.


**22 octobre 2026 — PR #120 fusionnée :** source HEAD `f7ef3ceeaee40bb90e1cb9fe180121f11867fc28`, [CI PR #39685054113](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39685054113) **SUCCESS terminale** (74 étapes Windows), fusion protégée `main=01766707a347a269b283c2aa7ea02f44979759e9`, [CI post-fusion #39686405108](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39686405108) **SUCCESS terminale au SHA exact**. Le cinquième module Rust de chronologie reste strictement `#[cfg(test)]`, utilise SQLite RAM et démontre un **successeur humain unique** après retrait d'une reformulation, avec graphe actif en ordre partiel. Aucun code de production/IPC n'est activé.

**Aucune promotion des gates :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT non fusionnable, writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, attestations historiques `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Aucun accès opérateur Windows, SQLite v6/v7 originale, backup, ACL, WAL/SHM, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release. Parallélisation autorisée pour lectures et travaux indépendants, mais commits sur même branche et merges séquentiels avec CI SHA exact.

**Prochain développement permis en source-only :** étudier une tranche **séparée** de révocation d'un successeur fictif (`m3_2_successor_revocations_candidate.sql`) avec conservation immuable de l'historique et refus des cycles, puis seulement plus tard les chaînes récursives dans un dossier distinct. Chaque incrément exige fixture SQLite RAM, branche propre, tests adversariaux et CI au HEAD exact. Les recherches sur les preuves historiques #36 et la baseline prospective #38 peuvent avancer en parallèle, sans inventer de preuves ni utiliser les fichiers Windows protégés.


**22 octobre 2026 — PR #119 MERGED sous Protect main :** source `0df96696e4abefe692f8a0fdca3ab10e726fa9d3`, CI PR #39661776335 SUCCESS (74 étapes, 121 tests Rust, 48 tests continuité, 21 inventaires SQLite, 50 Chromium par mode). Nouveau `main=61e07deaf10fc393c567e8f1960874b75d81adc4`, CI post-fusion #39684342539 **IN_PROGRESS_AT_CHECKPOINT** ; revérifier le résultat terminal au SHA exact.

**Cinquième tranche test-only candidate :** un successeur humain unique d'une reformulation retirée, `succeed_withdrawn_restatement`, lecture du graphe actif partiel par `list_active_precedence_graph` et SQL candidat `m3_2_restatement_successors_candidate.sql` sur SQLite exclusivement en RAM. Quatre nouveaux tests Rust : retrait obligatoire, unicité, cycles/doublons, ancres retirées et historique immuable. Aucune correction en chaîne, aucune révocation de successeur, aucune inférence de chronologie totale.

**STOP non levé :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, écrivain SQLite réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Pas de Windows opérateur, SQLite originale v6/v7, backups, ACL, sidecars, marker, migration 007, writer IPC, M3.3, ComfyUI ou release.


**21 octobre 2026 — PR #118 MERGED :** source `ff996fc27da6df12697d68a46b8580a3a33e30b3`, CI #39658544037 SUCCESS (74 étapes, 117 Rust, 46 contrats, 21 inventaires SQLite, 50 Chromium par mode), fusion protégée `main=a0942b9566d6de21cf73e55dce47c3797dcb7c81`. CI push #39660168071 **IN_PROGRESS_AT_CHECKPOINT** : ne pas prétendre sa réussite terminale sans re-fetch exact. Nouvelle tranche test-only, uniquement SQLite RAM : révocation immuable de reformulation, historique conservé, 4 tests Rust supplémentaires ; aucune écriture active supplémentaire déduite.

**STOP toujours effectif :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 OPEN/DRAFT, réel writer NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE, historique 21/3/2 PENDING_EXTERNAL_ATTESTATION, prospective NOT_STARTED. Pas de Windows opérateur, original SQLite v6/v7, backup, ACL, journal, marker, migration 007, IPC writer, M3.3 ni release.


**21 octobre 2026 — PR #117 fusionnée et CI post-fusion exacte confirmée :** source `99d78a46e61a0765b6673353900cea55eb039e74`, CI #39653506345 **SUCCESS** (74 étapes, 112 tests Rust, 44 tests de continuité, 21 tests d'inventaire, 50 Chromium par mode). Fusion protégée `main=b76e6c00c579bee36c194872e3679c48fe9788fa` ; CI post-merge #39655214998 **SUCCESS terminale** sur ce SHA. La règle permanente de parallélisation des tâches indépendantes est toujours en vigueur.

**Troisième tranche test-only candidate :** reprise strictement limitée de la reformulation humaine explicite d'une précédence révoquée (`restate_revoked_precedence`) et du SQL candidat `m3_2_active_precedence_candidate.sql` sur SQLite **uniquement en mémoire**. Cinq tests Rust supplémentaires prévus : source révoquée obligatoire, interdiction de cycle, unicité, conservation immuable et blocage d'ancres retirées / insertion brute abusive. Le module reste `#[cfg(test)]`, sans exposition Tauri, migration 007 ni donnée locale opérateur. Révocation des reformulations, successeurs et corrections en chaîne sont hors portée. CI nouvelle au HEAD exact requise.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT/non fusionnable ; absence d'écrivain SQLite réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, provenance `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune commande Windows opérateur, base v6 active/v7 isolée, sidecars, ACL, sauvegardes, activation marker, IPC writer, M3.3, ComfyUI ou release.


**21 octobre 2026 — PR #116 fusionnée et CI post-fusion vérifiée :** HEAD source `0b2555833c1a2c0152cba2185c8122f3d3ecbbae`, CI PR #39626827246 **SUCCESS** (74 étapes Windows ; 106 Rust dont 6 nouveaux tests RAM, 42 contrats de continuité, 21 inventaires SQLite, 50 Chromium par mode). Fusion protégée `main=388cb745888f9f2d4d0a07fce1ed19fad9b4a548`, CI post-merge #39628479487 **SUCCESS terminale au SHA exact**. PR #35 reste DRAFT/non fusionnable. Règle permanente de parallélisation inchangée.

**Deuxième tranche source-only candidate :** reprise bornée de `decide_anchor`, `decide_precedence`, `supersede_anchor_atomically`, `list_current_anchor_ids`, `list_current_precedence_ids`, `list_anchor_decisions` et de `m3_2_chronology_decisions_candidate.sql` historique. Module Rust `#[cfg(test)]` uniquement, SQL candidat chargé **après v6 et v7 fictifs en mémoire** ; six nouveaux tests Rust prévus pour révocation, conservation de l'historique, rollback transactionnel, Univers distincts, cycles/contraintes. Aucune migration 007, aucun IPC ni base réelle ; CI au HEAD candidat obligatoire. Les restatements et chaînes de corrections restent hors portée.

**STOP maintenu :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; `PROCESS_WRITER_ABSENCE=NOT_PROVEN`; G2-B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, baseline prospective `NOT_STARTED`. Aucune action opérateur Windows, SQLite active v6, isolée v7, sauvegarde, ACL, sidecar, marqueur, migration 007, writer IPC, M3.3, ComfyUI ou release.


**21 octobre 2026 — PR #115 fusionnée :** HEAD source `3f1c5676f7035398b61bc143a16eae5e115cdfbe`, CI PR #39619267259 **SUCCESS** (74 étapes, 40 tests de continuité, 60 Vitest fictifs, 50 Chromium par mode, 100 tests Rust au commit source). Fusion protégée `main=33846c8c6813acda5eda5089827f81df99175d2c` ; CI post-fusion #39620942276 **SUCCESS terminale au SHA exact**. La règle de parallélisation reste active. La PR #35 demeure OPEN/DRAFT non fusionnable ; le portage décrit ci-dessous est indépendant, strictement test-only, et ne constitue aucune autorisation de fusion de #35.

**Nouvelle tranche candidate source-only :** portage limité des opérations `create_calendar`, `create_anchor`, `create_precedence`, `list_anchors`, `list_precedences` du Rust historique de PR #35 vers un module `#[cfg(test)]` sur `main`, avec six tests utilisant exclusivement des bases SQLite **en mémoire**, les deux Univers fictifs, quatre temporalités, ordre humain explicite, cycles interdits et révisions immuables. **Aucun IPC**, pas d'activation du schéma v7 réel ou de migration 007, aucune ouverture des fichiers opérateur. Une nouvelle CI SHA exact doit encore qualifier cette tranche ; les fonctions de supersession de PR #35 ne sont pas portées dans cette étape.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, réel writer `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, historique 21/3/2 non résolu, baseline prospective `NOT_STARTED`, aucune opération Windows opérateur ni production v6, v7 isolée, backups, ACL, journaux, activation marker, migration 007, writer IPC, M3.3 ou release.


**21 octobre 2026 — PR #114 fusionnée et CI post-fusion vérifiée :** la [PR #114](https://github.com/LaurentCOLL1/Fabulaxiom/pull/114), source `8262659d58045c127fe4ee3ac56e6dd5681a9f5f` et [CI PR #39612803528](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39612803528) **SUCCESS (job Windows 74 étapes)**, a été fusionnée sous protection à `main=ddb23311f40f09c04983b164ccd7afa361698ea8`. La [CI main #39614175650](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39614175650) est **SUCCESS terminale** au SHA de fusion exact. La règle permanente de parallélisation des tâches indépendantes figure dans `HANDOFF_PROTOCOL.md` sur `main`, sans autoriser les opérations Windows privées.

**Décision inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`; PR #35 OPEN/DRAFT, GitHub `mergeable=false` au HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` et prospective `NOT_STARTED` ; absence d'écrivain réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucune migration 007, writer IPC, M3.3, release ni opération sur production v6/isolée v7, sauvegardes, ACL, sidecars, marqueurs ou Windows opérateur.

**Voies parallèles sûres à poursuivre :** A : réconciliation *source-only* de la PR #35, sur branche nouvelle et fixtures inventées ; B : étude documentaire des cinq témoins historiques (issue #36), sans falsifier la provenance ; C : examen du protocole de baseline prospective et du propriétaire SQLite non migrant (issue #38), sans lecture de sources privées. Ces études peuvent avancer en parallèle ; commits concurrents vers la même branche et merges restent séquentiels, avec re-fetch et CI exacte. [Plan borné de réconciliation](../qualification/M3_2_PR35_SAFE_RECONCILIATION_PLAN.md).


**Checkpoint GitHub confirmé le 21 octobre 2026 :** PR [#113](https://github.com/LaurentCOLL1/Fabulaxiom/pull/113) **MERGED** sous Protect main, HEAD source `6fd369de970e6e35d42c2162f197eb57009a1d42`, [CI exacte #39605681206](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39605681206) **SUCCESS** (74 étapes Windows, 60 Vitest atelier fictif, 50 Chromium par mode), `main=e74f1001c01eff1f37c8b35d97d4ef34f6fbccb3` et [CI post-fusion #39607280677](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39607280677) **SUCCESS terminale au SHA exact**. PR #35 reste OPEN/DRAFT, GitHub `mergeable=false` ; source réelle G2B–G6 non autorisée, absence d'écrivain SQLite réel `NOT_PROVEN`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`. Aucun geste opérateur local réalisé.

**Règle permanente de parallélisation :** dès que des tâches sont indépendantes, privilégier leur exécution simultanée (re-fetch/lecture GitHub, analyses de roadmap, recherches de preuves, tests sur fixtures isolées), avec périmètres et branches séparés. Sérialiser toute modification d'un même fichier/ref Git, les fusions, la qualification d'une CI par SHA exact et les décisions de sécurité. Aucun parallélisme ne permet de contourner un gate, un STOP ou une autorisation Windows. Voir [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md).


**21 octobre 2026 — résultat terminal post-fusion PR #112 :** la CI push [#39597532619](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39597532619) a terminé **SUCCESS** sur `main=3c489aa727129e4b090e2e80a49a93fb3fa95877`, SHA exact du merge #112. Les mentions plus anciennes « en cours au checkpoint » sont des photographies historiques, et ne décrivent pas l'état terminal. Cette mise à jour de la PR #113 impose une CI nouvelle sur son nouveau HEAD. M3.2 reste IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, writer réel NOT_PROVEN, G2B–G6 STOP, aucun essai Windows opérateur ni SQLite protégée.


**21 octobre 2026 — PR #112 fusionnée avec CI source exacte :** [PR #112](https://github.com/LaurentCOLL1/Fabulaxiom/pull/112) MERGED sous Protect main au SHA `3c489aa727129e4b090e2e80a49a93fb3fa95877` ; HEAD source `56c5d4d55a616469cda36c5fef7f63369a08bdb2`, [CI #39596187154](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39596187154) terminale **SUCCESS** au HEAD exact (74 étapes Windows, 60 Vitest d'atelier fictif, 50 Chromium par mode normal et CSP stricte). [CI push `main` #39597532619](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39597532619) **EN COURS AU CHECKPOINT** au SHA de fusion ; revérification terminale requise. Cette fonctionnalité fictive relie deux révisions immuables explicitement choisies à une chaîne de précédences humaines actives sans faire dépendre le temps du monde de l'ordre narratif.

**STOP inchangé :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT, G2-A metadata-only (accord ponctuel consommé), écrivain SQLite réel `NOT_PROVEN`, G2-B à G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucun Windows opérateur, base réelle v6/v7, sauvegarde, ACL, WAL/SHM, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release.


**Candidat de preuves du monde par révisions exactes — 21/10/2026 :** le laboratoire fictif permet de sélectionner deux scènes et leurs révisions immuables pour lire une chaîne de précédences **humaines actives** entre leurs ancres, lorsque chacune possède exactement une ancre courante. Dates, ordre narratif entre romans et révélations ne sont pas déduits. Historique/révisions étrangères/ambiguïté : refus ou indétermination. 60 Vitest et 50 Chromium par mode **à qualifier sur une nouvelle CI**. Aucune intégration `App.tsx`/Tauri/SQLite.

**STOP :** M3.2 IN_PROGRESS_NOT_ACCEPTED, PR #35 DRAFT, G2-A accord consommé, écrivain réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE. Aucun Windows opérateur, original SQLite v6/v7, sauvegarde/ACL/journal, migration 007, IPC writer, M3.3 ou release.


**Vérification terminale post-fusion #110 (21 octobre 2026) :** [CI `main` #39591429432](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39591429432) **SUCCESS terminale** sur le SHA exact `2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b` ; PR #110 MERGED. Les anciennes mentions « en cours » documentent uniquement un instantané antérieur. Cette normalisation dans la PR #111 nécessite sa **propre CI fraîche au HEAD modifié** ; les deux CI de #110 ne sont pas transférables. **M3.2 toujours IN_PROGRESS_NOT_ACCEPTED**, PR #35 DRAFT ; G2-A métadonnées avec accord consommé, absence d'écrivain réel NOT_PROVEN, G2B–G6 NOT_AUTHORIZED, G3 réel STOP_UNAVAILABLE ; aucune commande Windows opérateur, originale SQLite, migration 007, IPC writer, M3.3 ni release.


**Checkpoint GitHub confirmé le 21 octobre 2026 :** PR [#110](https://github.com/LaurentCOLL1/Fabulaxiom/pull/110) **MERGED** sous Protect main sur `main=2bf4b6a62ca22a21e1e7d34f5ead4e86dafe450b` ; source `f69e36a24aedda15222bb3a4e3a198ba57d0174a`, CI PR [#39577527093](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39577527093) **SUCCESS terminale sur ce HEAD** (74 étapes Windows, 55 Vitest d'atelier fictif et 48 Chromium par mode normal / précompilé strict CSP). CI push [#39591429432](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39591429432) **EN COURS AU CHECKPOINT** sur le SHA du merge : re-fetch terminal obligatoire. Les anciennes mentions « candidat » sont historiques ; aucune CI d'ancien SHA transférable.

**Sécurité inchangée :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 OPEN/DRAFT ; G2-A PASS sur métadonnées seulement (accord unique consommé), absence d'écrivain SQLite réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`. Aucune commande Windows opérateur, aucun original v6/v7, sauvegarde, WAL/SHM, ACL, marqueur, migration 007, IPC writer, M3.3, ComfyUI ou release.


**Candidat UX M3.2 sur données inventées :** prévisualisation sans écriture des conséquences d'une révocation de précédence humaine avant l'action, en indiquant si un autre chemin actif conserve l'ordre. Cibles 55 Vitest / 48 Chromium par mode, CI fraîche obligatoire. G2B–G6 fermés, M3.2 non acceptée.


**Checkpoint terminal vérifié le 21 octobre 2026 :** PR #108 fusionnée sur `main=ba4b8a599910cef6d1c76fa1e4fb561a0b45e631`, CI source #39572172593 SUCCESS (51 Vitest, 46 Chromium par mode), CI push post-fusion [#39573518324](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39573518324) **SUCCESS** au SHA exact. Mentions « en cours » ci-dessous historiques. M3.2 NON ACCEPTÉE, PR #35 DRAFT, écrivain réel NOT_PROVEN, G2B–G6 STOP. Aucune exécution opérateur ni mutation SQLite.


**Checkpoint public du 21 octobre 2026 :** PR [#108](https://github.com/LaurentCOLL1/Fabulaxiom/pull/108) MERGED sur `main=ba4b8a599910cef6d1c76fa1e4fb561a0b45e631`, CI exacte de PR #39572172593 SUCCESS (74 étapes Windows, 51 tests atelier, 46 Chromium dans deux modes). CI post-fusion #39573518324 **EN COURS au présent instantané**, résultat terminal à vérifier. Fonctionnalité exclusivement fictive de refus des anciennes sélections historiques ; M3.2 NON ACCEPTÉE, PR #35 DRAFT, G2B–G6 STOP, écrivain SQLite réel NOT_PROVEN.


**Nouvelle tranche M3.2 candidate, exclusivement fictive :** après correction d'une ancre, une sélection historique est signalée et ne peut plus servir de preuve temporelle courante ; changement d'Univers réinitialise les choix. 51 tests Vitest/46 Chromium prévus mais CI nouvelle à qualifier. Voir [handoff](HANDOFF_CURRENT.md). M3.2 non acceptée, G2B–G6 STOP.


**Vérification terminale (21 octobre 2026) :** la CI push main [#39567933461](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39567933461) après fusion protégée PR #106 est maintenant **SUCCESS** au `main=fbfc785afa6e5bdf92c337004d1bd2f925c4957a`. La CI PR #39566947725 avait déjà terminé SUCCESS (48 tests atelier, 44 Chromium par mode). Les anciens « en cours » sont des preuves historiques datées ; aucun nouveau gate ouvert : M3.2 NOT_ACCEPTED, G2B–G6 STOP, écrivain réel NOT_PROVEN. La présente PR documentaire demande une CI neuve au HEAD exact.


**Checkpoint GitHub 21 octobre 2026 :** [PR #106](https://github.com/LaurentCOLL1/Fabulaxiom/pull/106) fusionnée au `main=fbfc785afa6e5bdf92c337004d1bd2f925c4957a`. CI PR #39566947725 terminale SUCCESS (48 tests atelier / 44 Chromium dans les deux modes, 74 étapes Windows), CI push main #39567933461 **EN COURS au checkpoint**. Laboratoire fictif de preuve humaine uniquement ; aucun original SQLite/Windows, M3.2 non acceptée, PR #35 DRAFT, G2B–G6 STOP.


**Nouvelle tranche candidate source-only :** preuve des précédences humaines explicites déjà connues dans l'atelier fictif, à qualifier en 48 Vitest / 44 Chromium. Aucun lancement Windows opérateur ni promotion des gates ; [handoff courant](HANDOFF_CURRENT.md).

**Vérification terminale du 21 octobre 2026 :** CI push `main=997b60901e1f18a426eae3efa34ddb29c07b5721` [#39554622761](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39554622761) désormais **SUCCESS** au SHA exact, après PR #104 MERGED (CI PR #39553745685 SUCCESS, 42 Vitest atelier / 41 Chromium). Les mentions antérieures « en cours » sont des instantanés historiques. M3.2 non acceptée, G2-B–G6 STOP, writer absence NOT_PROVEN. Aucun test Windows opérateur.


**État GitHub daté du 21 octobre 2026 :** PR [#104](https://github.com/LaurentCOLL1/Fabulaxiom/pull/104) fusionnée sur `main=997b60901e1f18a426eae3efa34ddb29c07b5721`, CI PR #39553745685 SUCCESS (42 tests atelier/41 Chromium dans deux modes). CI push main #39554622761 **en cours au checkpoint** ; re-fetch requis avant toute déclaration terminale. M3.2 non acceptée, PR #35 DRAFT, G2B–G6 STOP. Les mentions « candidat » ci-dessous sont historiques.

**Candidat distinct après PR #102 (non qualifié) :** [comparaison fictive des trois ordres](../qualification/M3_2_FICTIONAL_THREE_ORDERS_EXPLANATION.md), sélection de scènes dans le laboratoire de navigateur uniquement ; cible 42 tests atelier / 41 Chromium au nouveau SHA. Aucune promotion G2B–G6, M3.2 NON ACCEPTÉE. Ce paragraphe n'est pas la preuve d'une CI réussie.

**Dernier checkpoint GitHub daté du 21 octobre 2026 :** PR [#102](https://github.com/LaurentCOLL1/Fabulaxiom/pull/102) fusionnée sur `main=1f0a8cd9a369106202b57102aa28915de65b7472` ; CI PR #39543328344 et CI push main #39544279201 SUCCESS aux SHA exacts. 36 tests Vitest atelier / 38 scénarios Chromium sur univers inventés. M3.2 NON ACCEPTÉE, G2-B–G6 STOP. Les étapes « candidat » antérieures demeurent historiques ; voir [HANDOFF_CURRENT](HANDOFF_CURRENT.md), puis refetch GitHub.

**Autorité datée au 21 octobre 2026 :** PR #100 fusionnée sur `main=bf59b28b437470a4759a5971968e8f00f9fa895c` ; CI PR #39533766395 et CI main #39534698504 SUCCESS au SHA exact. 32 tests fictifs Vitest / 36 Chromium vérifiés pour ce candidat, sans acceptation M3.2 ni autorisation G2B–G6. Les mentions anciennes « à qualifier » sont des instantanés historiques ; voir [HANDOFF_CURRENT](HANDOFF_CURRENT.md). Re-fetch obligatoire.

Ce dossier constitue la **mémoire de travail versionnée du projet**. Lire en priorité, dans cet ordre :

1. [HANDOFF_CURRENT.md](HANDOFF_CURRENT.md) : état opérationnel concis, dernier checkpoint vérifié et prochaine action.
2. [HANDOFF_CURRENT.json](HANDOFF_CURRENT.json) : mêmes barrières de sécurité en format vérifiable par CI, sans autorité d'exécution.
3. [HANDOFF_PROTOCOL.md](HANDOFF_PROTOCOL.md) : règles permanentes de reprise et de mise à jour.
4. [HANDOFF_HISTORY.md](HANDOFF_HISTORY.md) : étapes déjà fusionnées, pour éviter de refaire les mêmes audits.
5. [NEXT.md](NEXT.md), puis [STATE.md](STATE.md) : historique détaillé et plans antérieurs (certains en-têtes anciens ont un statut « en attente » depuis clos).
5a. [Roadmap V1, matrice courante](../roadmap/ROADMAP_STATUS_CURRENT.md) et [index des cinq plans](../roadmap/README.md) : M3.1 normalisée, M3.2 non acceptée, jalons M3.3–M9 non autorisés.
6. [M3_2_GATE_DECISION_CURRENT.md](M3_2_GATE_DECISION_CURRENT.md) : **état décisionnel courant** séparant G2-A PASS observé et G2-B à G6 non autorisés.
7. [M3_2_GATE_SNAPSHOT.md](M3_2_GATE_SNAPSHOT.md) : photographie **historique du 19 octobre**, pas l'état G2-A actuel.
8. [bloc historique PR #86](../qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md) : **déjà exécuté sur Windows une fois, résultat STOP_WEBVIEW2_PARENTAGE** ; ne pas relancer.
9. [nouveau candidat G2-A PID 0](../qualification/M3_2_G2A_PID_ZERO_CANDIDATE_REVIEW.md) : **exécuté une seule fois après accord explicite le 20 octobre 2026 : PASS de métadonnées locales seulement** ; toute réexécution nécessite un nouvel accord.

10. [Analyse source-only de l'absence d'écrivain SQLite](../qualification/M3_2_G2A_WRITER_ABSENCE_GAP_SOURCE_REVIEW.md) : aucun moyen d'accès aux originales et aucun déblocage G2-B/G3.

11. [Audit source-only des points d'entrée SQLite Rust](../qualification/M3_2_G3_RUNTIME_ENTRYPOINT_SOURCE_AUDIT.md) : six fonctions connues et 18 tests de dérive, G3 réel toujours STOP.

12. [Inventaire élargi des sites SQLite Rust](../qualification/M3_2_WIDE_RUST_SQLITE_SITE_INVENTORY.md) : 25 modules Rust/Tauri, surveillance textuelle et 18 tests de refus, sans inspection des bases.

13. [Prototype Rust de lecteur préouvert en RAM fictive](../qualification/M3_2_PREOPENED_QUERY_ONLY_RAM_READER_TOY.md) : 13 tests Rust sous feature non défaut et cfg(test), G3 réel toujours STOP.

14. [Deux connexions RAM fictives et preuve négative d'absence d'écrivain](../qualification/M3_2_SHARED_RAM_EXTERNAL_WRITER_NEGATIVE_PROOF.md) : 12 tests CI sur SQLite en mémoire, G3 toujours STOP.

15. [Atelier fictif d'édition chronologique M3.2](../qualification/M3_2_SYNTHETIC_MANUAL_CHRONOLOGY_LAB.md) : premier CRUD simulé en mémoire sur le laboratoire navigateur, 13 tests, **pas** une acceptation M3.2.

16. [Références exactes de scènes/révisions dans l'atelier fictif](../qualification/M3_2_FICTIONAL_SCENE_REVISION_EXACT_BINDING.md) : source immuable inventée, 22 tests atelier/34 cas navigateur annoncés, jamais une preuve d'accès G3 réel.

17. [Aperçu des conflits cycliques et liens bloquant une correction](../qualification/M3_2_FICTIONAL_CONFLICT_WITNESS_AND_CORRECTION_PREFLIGHT.md) : témoin de cycle fictif, 32 tests unitaires et 36 Chromium qualifiés sur la PR #100 (CI non transférable) ; aucune autorisation G3.

Pour une nouvelle conversation, copier seulement le [prompt court](RESUME_PROMPT.md). Le dépôt GitHub réel prévaut sur tout texte ou souvenir du modèle. Les SHA inscrits ici sont des **repères historiques**, jamais la preuve que GitHub n'a pas changé entre-temps.

Les PR qui modifient le code ou les procédures de M3.2 doivent aussi mettre à jour `HANDOFF_CURRENT.md` et `HANDOFF_CURRENT.json` ; un garde-fou CI refusera leur omission. Ce garde-fou ne met pas les fichiers à jour automatiquement : **le développeur doit inscrire une preuve juste, datée et vérifiable**. Seule une fusion réussie les rendra disponibles dans `main`.
