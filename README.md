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
- SQLite + FTS5 pour la persistance/recherche structurée ;
- intégration Ollama locale directe sur la boucle locale ;
- aucun runtime Python/FastAPI obligatoire pour M0/M1.

**M1 — Persistence and project foundation : IN PROGRESS**

M1.1 — SQLite foundation and migration runner est **COMPLETE + MERGED + NORMALIZED**.

M1.2 — Project hierarchy schema est **COMPLETE + MERGED + NORMALIZED**.

M1.3 — No-AI CRUD service est **COMPLETE + MERGED + NORMALIZED**.

M1.4 — Text revisions and provenance foundation est **COMPLETE + MERGED + NORMALIZED**.

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
- qualification Windows et CI déterministe.

La subdivision actuellement autorisée est :

**M1.5 — Backup and restore baseline**

Elle ajoutera la sauvegarde/restauration applicative contrôlée et sa validation d'intégrité. Les sauvegardes manuelles antérieures restent conservées jusqu'à qualification de cette nouvelle fonction. L'IA narrative et la recherche restent hors périmètre.

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — décisions d'architecture ;
- `docs/PRODUCT_SCOPE_V1.md` — périmètre fonctionnel V1.

## Développement

Chaque jalon doit produire un résultat utilisable, documenté, testé et reproductible avant le suivant.
