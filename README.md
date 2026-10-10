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

**Implémentation M2.5 fusionnée ; normalisation documentaire M2 en cours.** Le statut COMPLETE + MERGED + NORMALIZED ne prend effet qu'après fusion de la PR de normalisation dédiée.

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

**M2.5 — Interface de faits sourcés et revue humaine : implémentation fusionnée, normalisation finale en cours.** PR #29 fusionnée à `f1e7ea99d26ad3390c7c47bfb339f26d730a44f1` après la CI exacte #38040227617 (32/32 frontend, 72/72 Rust) et la qualification Windows isolée sans Ollama. L'écran React permet de saisir des faits sourcés ou non sourcés, citer la révision de scène historique exacte, consulter les sept statuts, l'historique de revue et confirmer explicitement l'approbation/révocation canonique. Tests Windows : 8/8 hiérarchie, 8/8 synchronisation, 9/9 faits, 10/10 revue ; audit indépendant SQLite v6 : 3 faits, 2 sources et 11 événements immuables dans une base isolée. La base réelle et les sauvegardes sont restées intactes. Voir `docs/qualification/M2_5_SOURCED_FACTS_REVIEW_UI.md`.

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

## Documentation d'autorité

- `docs/continuity/STATE.md` — état courant du projet ;
- `docs/continuity/NEXT.md` — prochaine étape autorisée ;
- `docs/roadmap/FABULAXIOM_ROADMAP_V1.md` — feuille de route V1 ;
- `docs/roadmap/M1_PERSISTENCE_PROJECT_FOUNDATION.md` — plan détaillé M1 ;
- `docs/roadmap/M2_NARRATIVE_ENTITIES_CANONICAL_FACTS.md` — plan détaillé M2 ;
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
