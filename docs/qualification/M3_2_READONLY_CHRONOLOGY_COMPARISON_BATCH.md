# M3.2 — Stage 30 : revue groupée des comparaisons chronologiques explicites

**Reference Python purement synthétique en mémoire, lecture seule. Aucune interface Windows, SQLite réelle, écriture, IPC, lecture de fichier, moteur d'IA ou accès aux archives opérateur.**

## Autorités live et prédécesseur

- Protected GitHub `main=f7eabfea74480d307b52d4b053730021efc95352` inchangée, PR #35 OPEN/DRAFT/non fusionnée.
- Stage29 `09e7f6a535e20b402e32c099be245a4b91651cf8` [Windows pull_request CI #38640818567](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38640818567) terminal **41/41 SUCCESS** avec 34 nouveaux tests. Ce succès ne qualifie **pas** le commit Stage30.

## Contrat de batch

`review_comparison_batch(snapshot, universe_id, pairs: tuple[tuple[str,str],...], filters=..., navigation_page_size=32, witness_page_size=16)` prend **1 à 16 paires ordonnées et explicitement choisies**, jamais des combinaisons automatiques de toutes les ancres. Les répétitions et inversions sont maintenues dans l'ordre exact de demande, avec numéros de requête **locaux** (ni rang temporel ni tri total). Les deux éléments de chaque paire passent par Stage29, donc Stage25 vérifie leur activité, leur Univers et les filtres ; Stage28 reconstitue les liens humains et expose uniquement la **première page** de justification, avec son curseur permettant une consultation ultérieure sous même contexte. Tous les sous-résultats restent **ID-only**, les étiquettes de calendrier, noms, révisions et dates fictives ne sont pas copiés.

Toute paire mal formée, historique retirée ou remplacée, d'un autre Univers, filtrée ou absente entraîne un **refus global** : aucun résultat partiel ne revient. Le DTO `SyntheticComparisonBatch` est figé avec `partial_results_authorized=false`, `editing_authorized=false`, `data_origin=synthetic_in_memory_reference_only`. L'ordre des demandes n'est jamais l'ordre du monde. `same` et `incomparable` ne produisent aucune précédence inventée. La sortie n'est ni une preuve signée, ni un jeton d'accès, ni une API Tauri activée.

Ce composant est un **orchestrateur borné** de références synthétiques existantes, pas un moteur optimisé pour de grands graphes. Il recompute chaque inspection séparément ; la limite de 16 paires ne garantit pas à elle seule une performance sur des archives réelles. Les curseurs conservent les règles de cohérence Stage24/28 et ne remplacent pas un contrôle d'accès côté Rust/SQLite.

## Nouvelle qualification requise (non acquise avant CI)

`tools/test_m3_2_chronology_comparison_batch_reference.py` introduit **41 tests** (ordre de demande, orientation inverse, répétitions, chemins transitifs, paires mêmes/incomparables, limite 16, entrées et filtres adversariaux, sélection historique ou hors Univers, refus atomique, curseurs de preuve séparés, 513 ancres, confidentialité, immutabilité et déterminisme). Le workflow ajoute une nouvelle étape Windows : exiger **42/42 terminal SUCCESS au SHA exact**, dont 41 tests Stage30 et les suites Stages 20-29, frontend/Rust/Tauri et provenances.

Statut opérateur global **`PENDING_EXTERNAL_ATTESTATION`** : 21 empreintes historiques, 3 observations récentes, 2 rôles non ancrés. Sept worktrees Windows, base M1.5 production restaurée v6, copie M3.1 v7 isolée, ACL et sauvegardes/manifestes intacts. PR #35 reste DRAFT ; aucune migration 007 normale, aucun writer IPC, aucune fusion ni progression M3.3.
