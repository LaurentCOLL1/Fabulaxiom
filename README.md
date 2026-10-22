# Fabulaxiom

Fabulaxiom est une application locale de création et de gestion d'histoires, de romans, de sagas et d'univers fictifs, avec mémoire narrative persistante et intégration Ollama.

## Principes du projet

- fonctionnement local-first, sans abonnement ni API cloud obligatoire ;
- conservation durable et vérifiable des textes et des faits narratifs ;
- séparation entre canon validé, brouillons, suggestions, variantes et informations incertaines ;
- traçabilité des faits jusqu'à leurs sources ;
- validation humaine avant toute promotion d'une suggestion IA vers le canon ;
- détection des incohérences avec distinction entre contradiction démontrée, suspicion et information insuffisante ;
- fonctionnement utile même sans IA ;
- priorité à la fiabilité de la mémoire narrative et à la maîtrise des modifications.

## État actuel

**22 octobre 2026 — PR #130 protégée MERGED :** source `f980e8e294f537f6b588ded56f6f79cc772558d6` ; [CI #39764830760](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39764830760) terminale SUCCESS (74 étapes Windows, 132 Rust, 63 contrats, 53/53 Chromium normal et CSP) ; fusion `main=8f330a4feff30092847e5bf180160efed174ebdd`. [CI post-main #39769613787](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39769613787) `IN_PROGRESS_AT_CHECKPOINT` ici : préserver cet instantané, vérifier le résultat terminal séparément.

**Candidat suivant — source-only :** dans le navigateur fictif, afficher explicitement la correction précédente et son ancienne relation humaine `avant/après`, sans inférer de nouvelle chronologie. Tests existants renforcés ; qualification neuve obligatoire avant fusion. `App.tsx` et le runtime restent inchangés.

**STOP strict :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, absence writer réel `NOT_PROVEN`, G2B–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`, attestations `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun Windows opérateur, SQLite originale v6/v7, backups, sidecars, ACL, marqueur, migration 007, writer IPC, M3.3, ComfyUI, release. Parallélisation seulement indépendante ; commits/merges séquentiels.

**22 octobre 2026 — PR #129 :** normalisation documentaire fusionnée (`main=8f4b84bdccf19842aa98b35defe8e84a02e769db`) ; [CI PR #39756548081](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39756548081) et [CI post-main #39758153975](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39758153975) terminales SUCCESS au SHA exact. M3.2 demeure `IN_PROGRESS_NOT_ACCEPTED` : pas d'écrivain réel prouvé, G2B–G6 non autorisés, aucune action sur bases SQLite protégées ou Windows opérateur. Travaux de laboratoire fictifs uniquement.

**M0 — Environment and architecture qualification : COMPLETE + MERGED + NORMALIZED**

Architecture retenue :

- Tauri 2 ;
- React + TypeScript ;
- cœur applicatif Rust/Tauri ;
- SQLite pour la persistance structurée (FTS5 est planifié pour M4) ;
- intégration Ollama locale directe sur la boucle locale ;
- aucun runtime Python/FastAPI obligatoire pour M0/M1.

**M1 — Persistence and project foundation : COMPLETE + MERGED + NORMALIZED**

M1.1 — SQLite foundation and migration runner est **COMPLETE + MERGED + NORMALIZED**.

M1.2 — Project hierarchy schema est **COMPLETE + MERGED + NORMALIZED**.

M1.3 — No-AI CRUD service est **COMPLETE + MERGED + NORMALIZED**.

M1.4 — Text revisions and provenance foundation est **COMPLETE + MERGED + NORMALIZED**.

M1.5 — Backup and restore baseline est **COMPLETE + MERGED + NORMALIZED**.

Le socle persistant comprend désormais :

- SQLite embarqué via rusqlite ;
- migrations transactionnelles versionnées ;
- clés étrangères activées et vérifiées par connexion ;
- schéma v2 Universe → Series optionnelle → Novel → Chapter → Scene ;
- IDs stables et immuables ;
- ordre déterministe des éléments frères ;
- contraintes d'intégrité inter-univers ;
- services Rust CRUD avec erreurs déterministes et transactions explicites ;
- commandes Tauri minces ;
- écrans/formulaires React utilisables pour toute la hiérarchie ;
- CRUD opérationnel avec Ollama arrêté ;
- révisions de texte de scène immuables, historique append-only et provenance par parent ;
- pointeur de révision courante et restauration non destructive ;
- migration SQLite v3 qualifiée sur Windows ;
- sauvegardes SQLite vérifiées avec noms non écrasants ;
- restauration vers une nouvelle base indépendante, avec activation contrôlée sans écraser la précédente ;
- conservation de l'historique de révisions et des sauvegardes antérieures ;
- qualification Windows et CI déterministe.

## M2 — Entités narratives et faits canoniques

**M2.1 à M2.5 : COMPLETE + MERGED + NORMALIZED.** PR #30 de normalisation fusionnée à `f13b4f8c249866ff60a19d7895b6cfaede56398a` après CI exacte #38041908126. Les fonctionnalités M2 décrites ci-dessous sont livrées ; cela ne signifie pas que la V1 est terminée.

M2.1 — Entity registry schema and migration est **COMPLETE + MERGED + NORMALIZED**.

SQLite v4 ajoute un registre d'entités narratives lié à chaque univers et une table d'alias. Les six types pris en charge au niveau schéma sont : personnages, lieux, organisations, objets, événements et règles du monde. Le schéma préserve les identifiants et les contraintes d'intégrité.

La migration réelle v3 → v4 a été qualifiée sur Windows avec une sauvegarde vérifiée de la base restaurée réellement active. Le contrôle a confirmé la conservation des données M1, notamment des trois révisions textuelles et du pointeur courant. Les sauvegardes opérateur préexistantes sont conservées.

**M2.2 — No-AI entity and alias CRUD : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

La PR #23 d'implémentation a été fusionnée à `ad7211fa2f292b8bd9812e299dbb6be96214eb89` après les qualifications Windows (13/13 tests interactifs, 21/21 frontend, 51/51 Rust, base SQLite active et historique vérifiés). Les formulaires React et services Rust/Tauri permettent de créer, consulter, renommer et supprimer des entités narratives ainsi que leurs alias, avec identifiants immuables, rejet des doublons d'alias par entité et garde de suppression des entités liées, même avec Ollama arrêté.

**M2.3 — Registre des faits et provenance exacte : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

La PR #25 est fusionnée à `e6e80c26316f11054348a18a235fd08c600e136e`. SQLite **v5** ajoute les tables STRICT `narrative_facts` et `fact_sources`. Les services **Rust/Tauri** permettent de créer et consulter manuellement des faits sourcés ou non sourcés, avec identifiants durables, citations rattachées aux révisions immuables des scènes, bornes d'octets UTF-8 et contrôles d'univers/transaction. Les opérations restent locales et ne requièrent pas Ollama.

La migration réelle v4 → v5 a été qualifiée sur Windows après une sauvegarde cohérente vérifiée. **8/8 contrôles d'interface**, **21/21 tests React** et **61/61 tests Rust** PASS ; les neuf entités, huit alias, trois révisions et leur pointeur courant ont été conservés. Voir `docs/qualification/M2_3_IMPLEMENTATION_GATE.md`.

**M2.4 — Statuts canoniques et service de revue humaine : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

Implémentation PR #27 fusionnée à `3a069572d00e1680c42b0f13b800e28687c5f0eb`. SQLite **v6** ajoute `fact_review_events`, un journal de décisions de revue `STRICT` dont les événements ne peuvent pas être modifiés ou supprimés par les commandes normales. Les fonctions Rust/Tauri permettent de consulter les statuts et l'historique, de demander une transition déterministe et d'approuver ou révoquer explicitement le canon. Sept statuts : `draft`, `suggestion`, `canon`, `variant`, `unknown`, `ambiguous`, `contradictory`.

Qualification : **21/21 tests frontend**, **71/71 Rust**, **8/8 contrôles existants de l'interface Windows**, **8/8 tests Rust de revue isolée**, migration réelle v5→v6 et conservation vérifiée de toutes les données historiques, sauvegardes et pointeurs. Voir `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md`.

**À distinguer :** le nom du relecteur est déclaré, non authentifié. Le service ne constitue pas un écran React de gestion de faits : aucun test d'interaction E2E de revue via la fenêtre Tauri n'est revendiqué. Ollama est facultatif et aucune promotion au canon n'est automatique.

**M2.5 — Interface de faits sourcés et revue humaine : COMPLETE + MERGED + NORMALIZED.** PR #29 fusionnée à `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` après la CI exacte #38040227617 (32/32 frontend, 72/72 Rust) et la qualification Windows isolée sans Ollama. L'écran React permet de saisir des faits sourcés ou non sourcés, citer la révision de scène historique exacte, consulter les sept statuts, l'historique de revue et confirmer explicitement l'approbation/révocation canonique. Tests Windows : 8/8 hiérarchie, 8/8 synchronisation, 9/9 faits, 10/10 revue ; audit indépendant SQLite v6 : 3 faits, 2 sources et 11 événements immuables dans une base isolée. La base réelle et les sauvegardes sont restées intactes. Voir `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`.

Une proposition distincte d'atelier visuel local ComfyUI pour les personnages, scènes et événements figure dans `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md`. Elle est **documentée mais non autorisée à l'implémentation**.

## Utilisations actuellement disponibles

- **Organiser un univers narratif** : créer une hiérarchie Univers → Série facultative → Roman → Chapitre → Scène ; modifier les noms et l'ordre dans les limites des garde-fous.
- **Rédiger et retrouver l'historique d'une scène** : sauvegarder de nouvelles révisions, consulter leur historique et changer la révision courante sans écraser les versions antérieures.
- **Gérer les personnages et éléments de l'univers** : ajouter des personnages, lieux, organisations, objets, événements et règles du monde, avec identifiants stables même en cas de noms identiques.
- **Gérer les alias** : créer plusieurs alias par entité, les renommer ou les supprimer ; les doublons sur une même entité sont refusés.
- **Protéger le projet** : créer des sauvegardes applicatives SQLite et restaurer une sauvegarde dans une nouvelle base sans écraser l'ancienne ; un marqueur sélectionne la base active.
- **Travailler hors IA** : les opérations précédentes restent disponibles sans Ollama ; le diagnostic Ollama est indépendant.

- **Saisir des faits depuis l'interface graphique (M2.5)** : ajouter un attribut/une valeur à une entité, facultativement préciser une validité temporelle fictive, distinguer les faits sans source et les faits avec citation vérifiable.
- **Choisir un passage exact de scène** : sélectionner une ancienne révision immuable, capturer une citation en octets UTF-8 même avec accents/émojis, puis retrouver cette révision indépendamment du texte courant.
- **Gouverner le canon manuellement** : distinguer brouillon, suggestion, canon, variante, inconnu, ambigu et contradictoire ; consulter l'historique non effaçable des revues ; approuver ou révoquer explicitement avec justification et confirmation.
- **Actualiser les modules** : les nouveaux univers et entités, ainsi que les révisions de scènes, deviennent disponibles dans l'espace des faits sans forcer la fermeture ou le rechargement complet.
- **Utiliser l'application sans Ollama** : les fonctions manuelles M2 ne requièrent ni modèle actif ni service distant. L'identité du réviseur est une étiquette déclarée, pas une authentification.

**Non encore livrés :** la chronologie et les connaissances des personnages (M3), les recherches FTS5/sémantiques (M4), la génération/extraction IA (M5), le moteur automatique de cohérence (M6) et l'atelier d'images ComfyUI. Ce dernier reste une proposition distincte (issue #19), même si ComfyUI fonctionne déjà localement.

## Prochaine étape : normalisation M3 puis M3.1 uniquement

La planification M3 a été fusionnée par la PR #31 à `68db746754e01b441870e0653f17f10ebfc7be2f`, après sa CI exacte #38050865413 (13/13 étapes Windows). Elle organise six phases distinctes : temps fictif et schéma, chronologie manuelle, relations historiques directionnelles, croyances/connaissances, révélations narrateur/lecteur et états narratifs évolutifs. Voir `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md`.

**Aucune fonctionnalité M3 n'est encore livrée.** Après la qualification et la fusion d'une normalisation documentaire indépendante, **seule M3.1** peut être développée dans une nouvelle PR. Toute migration SQLite v6→v7 sur la machine de production exige une sauvegarde cohérente préalable et une qualification Windows distincte. M3.2–M3.6, M4+ et ComfyUI ne sont pas autorisés par cette planification. L'atelier visuel ComfyUI reste une proposition future (issue #19).

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md` — plan détaillé M2 ;
- `docs/roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md` — plan gouverné M3, sans implémentation ;
- `docs/qualification/M3_PLANNING_POST_MERGE_NORMALIZATION.md` — qualification documentaire indépendante de la planification M3 ;
- `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md` — preuves de qualification M2.2 ;
- `docs/qualification/M2_3_IMPLEMENTATION_GATE.md` — qualification M2.3, sauvegarde v4 et migration Windows v5 ;
- `docs/qualification/M2_4_CANON_REVIEW_IMPLEMENTATION_GATE.md` — qualification M2.4, sauvegarde v5 et migration Windows v6 ;
- `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md` — qualification Windows M2.5, provenance et revue humaine ;
- `docs/qualification/M2_5_POST_MERGE_NORMALIZATION.md` — preuves et frontière de normalisation M2.5 ;
- `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` — proposition visuelle non implémentée ;
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — décisions d'architecture ;
- `docs/PRODUCT_SCOPE_V1.md` — périmètre fonctionnel V1.

## Développement

Chaque jalon doit produire un résultat utilisable, documenté, testé et reproductible avant le suivant.
