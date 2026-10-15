# M3.2 — Stage 29 : cohérence de sélection et localisation en navigation synthétique

**Maquette Python en mémoire, exclusivement en lecture seule. Aucun accès SQLite, aucune fenêtre React/Tauri, aucun réseau, service, archive opérateur, worktree ou contrôle d'autorisation réel.**

## Autorité re-fetchée et prédécesseur

- Main GitHub `f7eabfea74480d307b52d4b053730021efc95352` inchangée ; PR #35 OPEN/DRAFT/non fusionnée.
- Stage 28a `bbdf37046b2d1266aab19cfb05de08d123fa6e05` accepté sur [Windows pull_request CI #38635782899](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38635782899), **40/40 SUCCESS**, dont 30 tests de consultation paginée. Cet ancien workflow ne valide pas les octets du Stage29.

## Modèle Stage29

`tools/m3_2_chronology_selection_review_reference.py` expose `review_selected_witness(snapshot, universe_id, left_id, right_id, filters=..., navigation_page_size=32, witness_page_size=16, witness_cursor=None)`. Les extrémités sont explicitement sélectionnées. Stage25 revérifie leur état actif dans le même Univers et leur visibilité par les filtres ; Stage28 recalcule leur chaîne humaine et consulte la page de preuve demandée. Stage29 détermine pour chaque ID son **rang dans le résultat filtré suivant l'ordre d'insertion des sources**, puis crée un pointeur de navigation Stage24 cohérent avec l'Univers, le snapshot, les filtres bruts et la largeur de page. Il rouvre lui-même la page Stage24 pour vérifier que l'ID annoncé est effectivement à la position affichée.

`SelectedAnchorLocation` conserve uniquement ID, ordinal 1-based du filtre, ordinal de page, ordinal dans la page et curseur Stage24 éventuellement nul pour la première page. `SyntheticSelectionReview` est figé, contient les deux emplacements, le nombre d'ancres filtrées, la largeur de navigation et la page de justification Stage28. **Ces positions ne représentent jamais un ordre temporel fictif**, et le nombre de liens dans le témoin humain n'est pas le nombre d'événements ou de dates.

Les deux paginations sont indépendantes : une nouvelle largeur de navigation déplace uniquement les localisateurs et invalide leurs propres anciens curseurs ; les curseurs Stage28 demeurent liés au snapshot, au filtre, à l'ordre de sélection et à leur propre largeur de témoin. Un changement des extrémités/filtre/snapshot ne saurait autoriser une reprise silencieuse. Même-ID et incomparabilité restent des choix explicites sans lien fictif. Les données sont **ID-only**, sans calendrier, source révisée ou libellé. Aucun curseur n'est une signature, une preuve historique, un jeton d'accès ou une garantie d'identité.

## Qualification sur nouveau SHA

`tools/test_m3_2_chronology_selection_review_reference.py` apporte **34 tests synthétiques adversariaux** : visibilité cross-page, localisateurs compatibles Stage24, reprise témoin, filtres, isolement d'Univers, statut remplacé/retiré, 513 ancres, changement de largeur/snapshot/ID, refus invalides, JSON déterministe et absence d'écriture. Nouvelle étape Windows : exige **41/41 SUCCESS** sur le **nouveau SHA exact**, incluant toutes les suites Stage28 et les contrôles frontend/Rust/Tauri.

Statut global inchangé : `PENDING_EXTERNAL_ATTESTATION`, 21 empreintes historiquement ancrées, 3 observations récentes, 2 rôles sans attestation indépendante. Préserver M1.5 restaurée SQLite v6, copie M3.1 isolée v7, sept worktrees, sauvegardes, ACL et manifestes. PR #35 DRAFT ; pas de migration 007 normale, writer IPC, fusion ou M3.3.
