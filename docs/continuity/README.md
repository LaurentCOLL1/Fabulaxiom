# Fabulaxiom — Point d'entrée pour reprendre les discussions ChatGPT

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
