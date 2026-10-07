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

**M0 — Environment and architecture qualification : COMPLETE + MERGED**

Architecture retenue pour M0/M1 :

- Tauri 2 ;
- React + TypeScript ;
- cœur applicatif Rust/Tauri ;
- SQLite + FTS5 pour la persistance/recherche structurée à partir de M1 ;
- intégration Ollama locale directe sur la boucle locale ;
- aucun runtime Python/FastAPI obligatoire pour M0/M1.

Le socle desktop, le pont React → Tauri → Rust, l'accès Ollama local en lecture seule, les tests et la CI déterministe sont qualifiés.

**M1 — Persistence and project foundation est maintenant autorisé.**

La première subdivision est décrite dans :
`docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md`.

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — décisions d'architecture ;
- `docs/PRODUCT_SCOPE_V1.md` — périmètre fonctionnel V1.

## Développement

Chaque jalon doit produire un résultat utilisable, documenté, testé et reproductible avant le suivant.
