# M3.2 — Stage 25 : comparaison explicite de deux ancres filtrées (synthétique)

**Source de référence Python en mémoire seulement. Aucune utilisation des SQLite réelles, aucun Tauri IPC, React, Ollama, réseau, migration ou action sur archives/worktrees Windows.**

## Autorité de départ

- `main=f7eabfea74480d307b52d4b053730021efc95352` re-fetchée ; PR #35 OPEN/DRAFT/non fusionnée, prédécesseur `bbc506a83e194b57aadb36546ecfedd7828670d3`.
- Stage 24.2 : CI Windows pull_request [#38623834483](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38623834483) **completed/success 36/36 sur le SHA exact**. Les 50 tests de navigation Unicode/filtre sont qualifiés ; cela ne qualifie pas les nouveaux octets Stage 25.
- Stage 22 présentait des comparaisons sur un panneau complet de 512 ancres au plus ; Stage 23–24.2 rendent possible une navigation filtrée paginée de 513+ ancres. La comparaison explicite entre deux ancres actuellement visibles dans le résultat filtré devait être vérifiée indépendamment du numéro de page.

## Nouveau contrat isolé

`tools/m3_2_chronology_comparison_reference.py` définit `compare_filtered_anchors(snapshot, universe_id, left_anchor_id, right_anchor_id, filters=...)`, pour deux **IDs explicitement sélectionnés**. Avant comparaison, le prototype valide la forme des IDs, les filtres Stage24, la présence des deux ancres dans le même Univers filtré et leur statut **actif** ; les corrections et retraits historiques restent consultables dans Stage21–24 mais ne peuvent être utilisés comme assertions temporelles actives.

Seul `relative_world_order` Stage21 calcule `same / before / after / incomparable` par les relations **humaines explicites**, y compris transitives. Sans lien, les calendriers fictifs, labels textuels, date, numéros, ordre d'insertion, récit et révélation lecteur **n'impliquent aucun ordre**. Les ID de révision historiques ne sont pas substitués par une révision courante. Un résultat filtré traverse logiquement les pages sans utiliser de curseur comme autorité. Aucune pagination n'est modifiée, aucune vue complète de 512 ancres n'est requise.

Le DTO `FilteredOrderComparison` est figé ; `editing_authorized=false`, narration et révélation indisponibles, origine `synthetic_in_memory_reference_only`. `comparison_json` est une sérialisation déterministe, pas une signature, un contrôle d'accès, un contrat IPC activé ni une preuve d'archive. Une interface future doit revérifier identité, autorisation et snapshot dans Rust/SQLite : un curseur de l'interface ne saurait garantir ces propriétés.

## Qualification attendue, PAS encore acquise

`tools/test_m3_2_chronology_comparison_reference.py` comporte **26 tests synthétiques adversariaux** : relations directes/inverses/transitives, incomparabilité, calendriers fictifs, mêmes ID, sélection sous filtres, rejet hors filtre et hors Univers, refus des historiques remplacés/retirés, références de révisions non substituées, entrée invalide, plus de 512 ancres, déterminisme et immutabilité. Exiger **37/37 étapes Windows** terminales sur le **nouveau SHA exact** (nouvelle étape Stage25 + suites Stage24.2/23/22/21/20a, provenance, Rust/React). Aucune réussite héritée n'autorise le nouveau code.

Statut historique global **`PENDING_EXTERNAL_ATTESTATION`** : 21 SHA historiques attestés, 3 observations récentes, 2 rôles non ancrés. Préserver production M1.5 restaurée v6, copie isolée M3.1 v7, les sept worktrees Windows, ACL, manifestes et sauvegardes. PR #35 reste DRAFT ; aucune migration 007 automatique, écriture M3.2, fusion, ni M3.3.
