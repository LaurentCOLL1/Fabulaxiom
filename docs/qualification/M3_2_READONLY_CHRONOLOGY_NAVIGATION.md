# M3.2 — Stage 24 : navigation filtrée dans la chronologie (prototype synthétique)

**Source expérimentale Python, exclusivement en mémoire. Aucun composant React, IPC Tauri/Rust, accès SQLite, migration, connexion opérateur, action sur les sauvegardes, ni autorisation d'écriture.**

## Autorités et qualification précédente

- Dépôt protégé : `main=f7eabfea74480d307b52d4b053730021efc95352` au dernier re-fetch précédant le Stage 24 ; PR #35 OPEN/DRAFT/UNMERGED.
- Stage 23 : HEAD `3cb8a334098633cea321b1f76a6b58001260bd1d`, workflow Windows pull_request exact [#38605084315](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38605084315), **completed/success 35/35**. 28 tests Stage23, 25 Stage22, 25 Stage21, 25 Stage20a, 33 provenance, et contrôles Rust/React réussis.
- Stage 18.1 : contrôle physique réel de la seule base isolée M3.1 v7, en lecture seule, intégrité / FKs / schéma / SHA avant/après PASS. **M3.2 global PENDING_EXTERNAL_ATTESTATION** : 21 empreintes historiquement ancrées, 3 observations récentes et 2 références non ancrées. Aucune attestation indépendante nouvelle.
- Stage 23 ne fait pas une interface de chronologie ; sa pagination repose sur l'ordre d'insertion source, jamais sur une conversion fictive en dates.

## Modèle Stage 24 en mémoire

`tools/m3_2_chronology_navigation_reference.py` définit :

- `NavigationFilters` figé : sélection facultative de statuts `active`, `replaced`, `withdrawn` ; types `exact`, `approximate`, `relative`, `unknown` ; égalité stricte d'un `calendar_id` ou d'un `source_revision_id` ; recherche textuelle littérale `text_contains` (insensible à la casse) sur `exact_label`, bornes de fenêtre et `precision_text`.
- `navigate_chronology(snapshot, universe_id, filters, page_size, cursor)` : filtre **avant** pagination dans le seul Univers explicitement demandé ; restitue les cartes `AnchorCard` existantes, avec identifiants, sources et lignées immuables.
- `NavigationPage` : `anchor_cards`, `total_matches`, `next_cursor`, `previous_cursor`, `display_order_semantics=source_insertion_order_not_world_time`, `editing_authorized=false` et `data_origin=synthetic_in_memory_reference_only`.
- `navigation_json` : sérialisation déterministe d'un DTO, pas une API utilisateur connectée.

Le statut historique d'une ancre remplacée/retirée n'est pas supprimé et peut être filtré ; aucune rectification ou retrait n'est créé par navigation. Les identifiants de révision demeurent historiques et ne sont pas remplacés par une tête « dernière version ». La recherche textuelle traite **uniquement des chaînes littérales**, sans interprétation des calendriers, OCR, NLP, géolocalisation ou comparaison chronologique. Les relations `before/after/incomparable` du Stage21 ne sont pas transformées en tri implicite.

## Curseur lié au filtre et au snapshot

Le contrat réutilise le parseur de curseur synthétique strict du Stage23. L'empreinte de cohérence de pagination inclut désormais **la représentation du snapshot entier ET les filtres demandés**. Reprendre avec un autre Univers, un snapshot modifié ou un filtre changé est refusé. Le curseur précédent réouvre la page antérieure pour le même ensemble filtré ; la première page n'a pas de curseur précédent.

**Cette empreinte n'est pas un MAC, une signature, un jeton d'autorisation ni une preuve d'intégrité archivistique.** Une interface réelle devrait autoriser l'accès au niveau Rust et conserver un snapshot DB cohérent séparément. Le booléen d'édition reste faux ; un curseur forgé ne doit jamais autoriser une écriture.

## Bornes et invariants

- Page : 1 à **64** cartes au maximum ; sous-ensemble de 513+ ancres synthétiques paginable sans déclencher le veto de la vue complète Stage22.
- Recherche : 1 à **128** caractères non blancs ; filtres d'identifiant calendaire/révision limités à 256 caractères.
- Sélections : rejet des statuts inconnus, types inexistants, doublons, champs vides, tailles booléennes, mauvais types, curseurs périmés ou hors Univers.
- Les résultats d'un Univers ne divulguent jamais les identifiants historiques d'un autre Univers. Un total de zéro éléments donne une page vide et aucun curseur.
- Ordre d'affichage stable de la source ; **pas** d'ordre temporel total présumé. Les limites sont celles du prototype, pas une politique définitive de production.

## Qualification Windows requise

`tools/test_m3_2_chronology_navigation_reference.py` ajoute **35 scénarios synthétiques** : filtrage par statuts et types, sélection d'Univers, calendrier et révision, recherche de chaînes brutes, combinaison de filtres, parcours multi-pages, navigation précédente, 513 ancres, rétractations conservées, curseurs périmés après changement de filtre/snapshot, contrôle des entrées invalides, sérialisation déterministe, interdiction d'écriture et invariants d'immutabilité. La nouvelle CI doit valider **36 étapes terminales** sur le SHA exact, dont les 35 nouveaux tests et toutes les suites antérieures.

La réussite du SHA Stage23 n'est pas transférable. La réussite de Stage24 confirmerait seulement le **prototype synthétique** ; elle ne fournirait aucune attestation des fichiers ACL ou de la base réelle.

## Interdictions maintenues

Préserver les **sept** worktrees historiques, la production restaurée M1.5 SQLite v6, la copie M3.1 v7 isolée, les manifestes et sauvegardes ainsi que les deux fichiers d'ACL. Aucun 8e worktree, aucune activation automatique de la migration `007`, aucune nouvelle identité d'écriture M3.2, aucune interface React/Tauri de mutation, aucune fusion de PR #35 et aucun M3.3 tant que les attestations externes demeurent non établies.

Références : https://docs.python.org/3.12/library/dataclasses.html ; https://docs.python.org/3.12/library/json.html .
