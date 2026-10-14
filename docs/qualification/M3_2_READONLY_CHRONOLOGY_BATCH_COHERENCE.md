# M3.2 — Stage 31 : cohérence des paires groupées explicitement demandées

**Référence Python exclusivement synthétique, immuable, en mémoire et lecture seule. Aucune donnée SQLite réelle, sauvegarde opérateur, archive historique, fichier, IPC, service ou application Windows n'est manipulée.**

## Autorités re-fetchées et prédécesseur

- `main=f7eabfea74480d307b52d4b053730021efc95352` inchangée ; PR #35 OPEN/DRAFT non fusionnée.
- Stage30 `ebd022872a9f0e4a54e2f73407fb9e142139756a` — [Windows pull_request #38642688135](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38642688135) `completed/success` **42/42**, 41 tests synthétiques Stage30.
- Ce résultat ne valide **pas** de nouvelles modifications Stage31.

## Contrat

`audit_comparison_batch(snapshot, universe_id, pairs, filters, navigation_page_size, witness_page_size)` reconstitue **depuis les seules entrées explicites** le lot Stage30 (1..16 paires), puis contrôle son intégrité par `_check_batch_consistency`. Chaque paire est vérifiée individuellement sur le même snapshot, dans un seul Univers et sous les filtres en vigueur, y compris les versions historiques retirées/remplacées et les ancres absentes. Aucun objet de preuve fourni arbitrairement par l'appelant n'est utilisé pour établir l'ordre temporel.

Le groupement ne concerne que les paires d'identifiants **strictement identiques à orientation près**, déjà demandées. La première requête détermine seulement l'identifiant ordinal local du groupe ; une répétition garde la même relation et le même chemin humain ; une paire inversée doit avoir la relation inverse (`before↔after`, `same↔same`, `incomparable↔incomparable`) et la même première page de liens de précédence originaux. Toute discordance détectée rejette l'ensemble du lot ; aucun résultat partiel n'est rendu. Le contrôle défensif sur DTO corrompu n'accorde aucune confiance ou permission à ce DTO.

`SyntheticBatchCoherence` contient le batch Stage30 intact et une liste figée `PairConsistencyEntry` dans l'ordre de demande, la première requête du groupe, l'ordinal de groupe et l'orientation `first/repeated/reversed`. Les ordinals de demande, groupe, navigation et liens sont **sans signification chronologique**. **Aucun nouvel ordre du monde n'est déduit entre paires différentes**, y compris lorsque des relations transitives existent dans les déclarations humaines. Ni tri total, ni lecture de calendrier fictif, ni fusion avec l'ordre narratif ou celui des révélations.

Les sorties demeurent **ID-only**, avec `editing_authorized=false`, `data_origin=synthetic_in_memory_reference_only`, et `cross_pair_temporal_inference=not_attempted`. La sérialisation déterministe n'est ni signature, ni preuve de garde des archives, ni interface IPC ni mécanisme de contrôle d'accès.

## Qualification requise (en attente)

`tools/test_m3_2_chronology_batch_coherence_reference.py` contient **37** scénarios déterministes/adversariaux : inversions, répétitions, mêmes/incomparables, preuves strictes, limites 16, invalides historiques et multi-Univers, filtres, 513 ancres, falsification défensive d'ordinals/relation/justificatifs internes, JSON, immutabilité et aucune fuite de labels. Le workflow Windows ajoute une étape et exige **43/43 terminal SUCCESS sur le SHA exact**, avec la totalité des tests de provenance, frontend/Rust/Tauri et lockfiles ; la CI précédente 42/42 ne suffit pas.

Le statut opérateur historique reste **`PENDING_EXTERNAL_ATTESTATION` (21/3/2)**. Préserver les sept worktrees Windows, la SQLite production M1.5 restaurée v6, la v7 M3.1 isolée, ACL, manifestes, archives et sauvegardes. PR #35 DRAFT, aucune migration 007, aucun writer IPC, fusion ou M3.3.
