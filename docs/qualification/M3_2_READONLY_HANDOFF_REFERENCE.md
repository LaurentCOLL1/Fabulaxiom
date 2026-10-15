# M3.2 — Stage 32 : contrat de présentation synthétique pour une future interface en lecture seule

**Exclusivement référence Python en mémoire, non intégrée : aucune commande Tauri, aucun composant React, aucun accès SQLite ou fichier, aucune lecture opérateur et aucune attestation.**

## Prédécesseur et source exacte

- `main=f7eabfea74480d307b52d4b053730021efc95352` inchangée, PR #35 OPEN/DRAFT/non fusionnée.
- Stage31 `306860ac777f49f0ee3e4602b18d9f8d54bdff76` [CI Windows pull_request #38647066177](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38647066177) terminal **43/43 SUCCESS** avec 37 nouveaux tests. Ce résultat ne peut qualifier Stage32.

## Contrat réduit et blocages visibles

`build_readonly_chronology_handoff(snapshot, universe_id, pairs, filters, navigation_page_size, witness_page_size)` **recalcule** Stage31 depuis un snapshot synthétique et 1..16 paires expressément fournies ; il ne consomme aucun rapport JSON/DTO comme preuve externe. Il retourne une projection **ID-only**, regroupée dans l'ordre des requêtes : ID gauche/droit, numéros locaux de requête et groupe, orientation répétée/inversée, relation humaine `before/after/same/incomparable`, clés de message d'affichage, rangs de navigation par ordre d'insertion des sources, IDs des liens de précédence présents sur la première page, nombre total de liens et indicateur de continuation. Il ne transmet ni textes des calendriers fictifs, ni source revision, ni dates converties, ni curseur transporté vers un consommateur inconnu.

Le résultat figé `ReadonlyChronologyHandoff` contient systématiquement `runtime_integration=not_implemented`, `database_access=none`, `write_commands=()`, `editing_authorized=false`, `external_attestation_verified=false`, `operator_acceptance_verified=false`. Les raisons de blocage sont des avertissements de **non-vérification par ce simulateur**, pas des mesures dynamiques de l'environnement. La sortie JSON est une **démonstration déterministe** ; elle ne doit pas être activée comme API ou assimilée à une preuve cryptographique.

Les deux autres dimensions demeurent explicitement indisponibles : ordre narratif et ordre des révélations au lecteur. Les ordinals représentent l'ordre d'affichage des sources, jamais un classement temporel total. Toute paire retirée/remplacée, absente, hors Univers ou cachée par les filtres annule le résultat entier.

## Qualification distincte requise

`tools/test_m3_2_chronology_readonly_handoff_reference.py` ajoute **34 tests synthétiques** : relations directes, inverses, transitives, même-ID/incomparables, répétitions, limite 16, 513 ancres, vérification des blocages, absence de commandes, refus des entrées et des historiques invalides, déterminisme et confidentialité. Exiger **44/44** succès Windows terminal sur le nouveau SHA exact, y compris toutes les suites antérieures.

`PENDING_EXTERNAL_ATTESTATION` 21/3/2 demeure l'autorité historique. Les sept worktrees, production M1.5 restaurée v6, copie M3.1 v7 isolée, ACL, sauvegardes et manifestes demeurent hors périmètre. Aucun éditeur, IPC, migration 007 normale, fusion PR #35 ou M3.3.
