# M3.2 — témoins de conflits et corrections de chronologie sur fixtures inventées

**Checkpoint source-only : 21 octobre 2026.** Base GitHub vérifiée : `main=205a328150c90bf1fb4f52abd7fb8c04f3959468`, PR #99 fusionnée, CI PR #39480662913 SUCCESS au HEAD exact, CI post-fusion #39482419125 SUCCESS. Aucune autorisation nouvelle pour Windows, SQLite ou G2–G6.

## Livrable et limites

Le laboratoire navigateur **exclusivement fictif** de M3.2 propose désormais un aperçu explicatif et non destructif **avant** toute commande manuelle. Le modèle `src/m32FictionalManualChronology.ts` ajoute deux fonctions pures :

- `previewFictionalPrecedence` examine seulement les ancres et relations `current` d'un univers fictif validé. Pour une demande `X avant Y`, il explore les liens existants de `Y` vers `X` par parcours en largeur déterministe (ordre alphabétique des identifiants) : si un chemin existe, ajouter la relation créerait un cycle. Il retourne le chemin explicatif et **les ID précis des relations utilisées**, sans fabriquer une date, un ordre total ou une connaissance canonique. Pour une paire vide, étrangère, réflexive ou déjà déclarée, il exprime un refus distinct.
- `previewFictionalCorrection` affiche les ID des relations actives liées à l'ancre que l'utilisateur veut remplacer et **l'ID de sa révision historique**, si elle existe. Il ne révoque jamais les relations pour l'utilisateur : les corrections qui nécessitent une révocation explicite restent bloquées.

Les véritables actions `createFictionalPrecedence` et `supersedeFictionalAnchor` réutilisent ces fonctions de prévisualisation pour rejeter les propositions dangereuses au moment de leur exécution, et non uniquement lors de l'affichage. Le composant React `src/M32ManualChronologyLab.tsx` affiche deux aperçus dans le laboratoire isolé, sans modifier `App.tsx`, le pont Rust, Tauri, Ollama ou SQLite. Les événements fictifs restent en mémoire et sont reconstruits à chaque changement de scénario.

Le comportement respecte la distinction prévue par la [roadmap M3](../roadmap/M3_TIME_KNOWLEDGE_RELATIONSHIPS.md) : chronologie du monde partielle, narration indépendante, révélation non inventée. Les parcours de graphe en mémoire suivent un principe analogue aux [requêtes récursives sur graphes décrites par SQLite](https://www.sqlite.org/lang_with.html), sans utilisation de SQLite dans ce prototype. Les mises à jour de l'état React sont produites sans mutation, conformément aux [recommandations React](https://react.dev/learn/updating-arrays-in-state).

## Preuves proposées (CI obligatoire au HEAD final)

- `src/m32ManualChronologyLab.test.tsx` : **10 nouveaux tests**, portant la suite ciblée à **32 tests**, vérifiant cycle `C → A → B → C`, IDs du témoin, liens doubles, paire vide, ancre étrangère, ordre partiel, révocation et conservation des révisions, audit immuable et aperçu dans l'interface.
- `tools/m32_browser_interaction.cjs` : **2 nouveaux scénarios Chromium**, portant les interactions à **36**. Le navigateur doit afficher le témoin `human-ab / human-bc` *avant* que l'utilisateur clique, et montrer la possibilité d'une correction après révocation manuelle du lien bloquant. Les cas de refus CSP, provenance Git, session fictive et multiunivers restent en place.
- Les deux listes blanches de fichiers fictifs restent **exactement à neuf sources**. Aucune dépendance ni requête réseau ajoutée.

**L'atelier n'est pas la fonctionnalité M3.2 acceptée.** Il ne prouve pas la sérialisation, les transactions, le propriétaire SQLite, la sauvegarde, la synchronisation entre connexions, la qualification Windows opérateur ou la normalisation finale. Une prévisualisation utilisateur n'est jamais une autorisation de mutation des véritables bases.

## Barrières intactes

M3.1 `COMPLETE_MERGED_NORMALIZED`; M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 toujours DRAFT. G2-A `PASS_METADATA_ONLY_OWNER_REPORTED` après une seule autorisation consommée, `PROCESS_WRITER_ABSENCE=NOT_PROVEN`. G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Provenance historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucune lecture/mutation des bases v6/v7 de l'opérateur, leurs journaux et sidecars, ACL, sauvegardes, marqueurs, migration 007, writer IPC, M3.3, ComfyUI ou release. Toute opération locale future requiert la procédure exacte affichée au préalable et un nouvel accord explicite.
