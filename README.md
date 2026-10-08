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

Le prochain jalon de la feuille de route est :

**M2 — Narrative entities and canonical facts**

**PLANNING AUTHORIZED — implementation subdivision not yet authorized.**

M2 nécessite d'abord une roadmap détaillée, des subdivisions ordonnées, des règles de validation humaine et des critères de qualification explicites. Aucune extraction IA ni fonctionnalité M2 n'est encore implémentée ou autorisée.

Les anciennes sauvegardes opérateur M1.2 et M1.4 restent conservées.

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — décisions d'architecture ;
- `docs/PRODUCT_SCOPE_V1.md` — périmètre fonctionnel V1.

## Développement

Chaque jalon doit produire un résultat utilisable, documenté, testé et reproductible avant le suivant.
