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

**IN PROGRESS**

M2.1 — Entity registry schema and migration est **COMPLETE + MERGED + NORMALIZED**.

SQLite v4 ajoute un registre d'entités narratives lié à chaque univers et une table d'alias. Les six types pris en charge au niveau schéma sont : personnages, lieux, organisations, objets, événements et règles du monde. Le schéma préserve les identifiants et les contraintes d'intégrité.

La migration réelle v3 → v4 a été qualifiée sur Windows avec une sauvegarde vérifiée de la base restaurée réellement active. Le contrôle a confirmé la conservation des données M1, notamment des trois révisions textuelles et du pointeur courant. Les sauvegardes opérateur préexistantes sont conservées.

**M2.2 — No-AI entity and alias CRUD : COMPLETE + MERGED + NORMALIZED** après fusion de la PR de normalisation dédiée.

La PR #23 d'implémentation a été fusionnée à `ad7211fa2f292b8bd9812e299dbb6be96214eb89` après les qualifications Windows (13/13 tests interactifs, 21/21 frontend, 51/51 Rust, base SQLite active et historique vérifiés). Les formulaires React et services Rust/Tauri permettent de créer, consulter, renommer et supprimer des entités narratives ainsi que leurs alias, avec identifiants immuables, rejet des doublons d'alias par entité et garde de suppression des entités liées, même avec Ollama arrêté.

**M2.3 — Registre des faits et provenance exacte : prochaine subdivision autorisée uniquement après la normalisation M2.2.** Le stockage de faits canoniques, leur validation et l'extraction IA ne sont pas livrés à ce stade.

Une proposition distincte d'atelier visuel local ComfyUI pour les personnages, scènes et événements figure dans `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md`. Elle est **documentée mais non autorisée à l'implémentation**.

## Utilisations actuellement disponibles

- **Organiser un univers narratif** : créer une hiérarchie Univers → Série facultative → Roman → Chapitre → Scène ; modifier les noms et l'ordre dans les limites des garde-fous.
- **Rédiger et retrouver l'historique d'une scène** : sauvegarder de nouvelles révisions, consulter leur historique et changer la révision courante sans écraser les versions antérieures.
- **Gérer les personnages et éléments de l'univers** : ajouter des personnages, lieux, organisations, objets, événements et règles du monde, avec identifiants stables même en cas de noms identiques.
- **Gérer les alias** : créer plusieurs alias par entité, les renommer ou les supprimer ; les doublons sur une même entité sont refusés.
- **Protéger le projet** : créer des sauvegardes applicatives SQLite et restaurer une sauvegarde dans une nouvelle base sans écraser l'ancienne ; un marqueur sélectionne la base active.
- **Travailler hors IA** : les opérations précédentes restent disponibles sans Ollama ; le diagnostic Ollama est indépendant.

Ces fonctionnalités sont distinctes des projets futurs (faits et canon humain M2.3–M2.5, chronologie, recherche sémantique, aide à l'écriture et atelier ComfyUI), qui **ne sont pas encore implémentés**.

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md` — plan détaillé M2 ;
- `docs/qualification/M2_2_ENTITY_ALIAS_CRUD.md` — preuves de qualification M2.2 ;
- `docs/roadmap/V1_VISUAL_REFERENCES_COMFYUI_PROPOSAL.md` — proposition visuelle non implémentée ;
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — décisions d'architecture ;
- `docs/PRODUCT_SCOPE_V1.md` — périmètre fonctionnel V1.

## Développement

Chaque jalon doit produire un résultat utilisable, documenté, testé et reproductible avant le suivant.
