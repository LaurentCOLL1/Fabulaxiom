# M3.2 — Réconciliation contrôlée de la PR #35 (plan source-only)

**Date d'observation :** 21 octobre 2026. **PAS UNE AUTORISATION DE FUSION NI UNE QUALIFICATION WINDOWS.** Ce fichier n'instruit aucune commande Windows opérateur.

## Etat GitHub au checkpoint

- `main=ddb23311f40f09c04983b164ccd7afa361698ea8`, protégé par le ruleset `Protect main`.
- PR #35 **OPEN/DRAFT**, HEAD `41ce7b915e76d22785d53d7fffe288d113dd0bf5`, base historique `f7eabfea74480d307b52d4b053730021efc95352`. GitHub signale `mergeable=false`.
- La comparaison GitHub du HEAD principal avec l'ancienne base de PR #35 signale **472 commits** en avance, **152 chemins modifiés** sur main, **84 fichiers** modifiés dans la PR #35. **7 chemins dont les noms apparaissent des deux côtés** : `.github/workflows/m0-ci.yml`, `docs/continuity/NEXT.md`, `docs/continuity/STATE.md`, `src-tauri/Cargo.toml`, `src-tauri/src/lib.rs`, `src/M32ChronologyPreview.tsx`, `src/m32ChronologyPreview.test.tsx`. Un chevauchement de noms ne prouve PAS 7 conflits textuels ; ne pas inférer non plus que tous les autres chemins sont directement compatibles.
- Le service `src-tauri/src/m32_manual_chronology.rs` est aujourd'hui **test-only** dans la PR #35. Les composants React chronologiques fictifs fusionnés depuis ne constituent pas un IPC Tauri réel.

## Voies parallèles, dépendances et livrables

| Flux indépendant | Travail autorisé sur données fictives/sources publiques | Condition de sortie |
| --- | --- | --- |
| A — service chronologique | Inventorier les signatures du Rust test-only de #35, les migrations candidates, décider ce qui est encore pertinent, rapprocher du modèle UI actuel **sur nouvelle branche** sans migrer ni lancer Tauri privé | Tests Rust/TS uniquement sur fixtures inventées, diff borné et preuve de non-regression |
| B — preuve historique | Rechercher de véritables témoins antérieurs pour les 5 rôles listés dans l'issue #36 | Vérification indépendante **authentique**, sinon `PENDING_EXTERNAL_ATTESTATION(21/3/2)` |
| C — sûreté / nouvelle baseline | Examiner uniquement les contrats source du propriétaire SQLite non migrant et les préconditions G2/G3 ; garder la baseline prospective comme `NOT_STARTED` | Aucun G2B–G6 autorisé sans dossier et accord individuel |
| D — intégration | Tester / documenter / re-fetch CI, HEAD, reviews et ruleset, consolider les dossiers de continuité | Sérialiser les écritures et fusions, CI terminale au HEAD exact, `expected_head_sha` |

### Ordre contrôlé pour le flux A

1. Lire l'état public exact de la PR #35 et le `main` courant ; **ne pas** fusionner directement cette PR brouillon et ne pas modifier la branche historique.
2. Relever les contrats utiles du service, des SQL candidats et des tests. Différencier propriétés métier (ancres, calendriers, relations, révisions exactes) de tout mécanisme d'accès à la base réelle.
3. Porter sur une **branche indépendante neuve** uniquement les éléments test-only pertinents, en privilégiant la structure de code actuelle de `main`. Examiner séparément les sept zones potentiellement chevauchantes et les autres 77 chemins.
4. Couvrir les quatre temporalités, deux Universes, plusieurs romans, cycles, superpositions, corrections par supersession/révocation, références de révisions historiques et séparation du temps du monde de la narration / révélation.
5. Soumettre la PR sous le protocole de protection, CI neuve SHA exact, revue des logs ; **aucun writer IPC**, aucun schéma v7 activé sur l'original, aucune promotion M3.2. Les tests sur fixtures ne certifient pas le système Windows opérateur.
6. Réévaluer plus tard les décisions G2B–G6 seulement après une autorisation propre et un mécanisme indépendant de provenance / sécurité, jamais par une simple réussite CI.

## STOP invariant

M3.2 `IN_PROGRESS_NOT_ACCEPTED`, PR #35 `OPEN/DRAFT` et non fusionnable, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, écrivain SQLite réel `NOT_PROVEN`, G2-B/C/D et G3–G6 `NOT_AUTHORIZED`, vrai G3 `STOP_UNAVAILABLE`. Aucun accès ou mutation de la SQLite active v6, de la v7 isolée, des backups, ACL, journaux/sidecars, activation markers et worktrees privés. Pas de migration 007, writer IPC, M3.3, ComfyUI ni release. Aucune exécution Windows opérateur par ce plan.
