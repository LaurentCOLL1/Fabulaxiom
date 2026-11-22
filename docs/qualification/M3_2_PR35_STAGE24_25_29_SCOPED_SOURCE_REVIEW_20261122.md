# PR #35 — portée distincte des étapes Python Stage 24 / Stage 25 / Stage 29 (22/11/2026)

**CANDIDAT DOCUMENTAIRE, NON QUALIFIÉ PAR SA PROPRE CI, NON ADMIS.** Analyse source-only préparée pendant PR #417, reportée sans portage sur son nouveau parent protected `main=10f34444533d0a8a6760378f71a92a9e5c6fa57e`. La PR #417 est MERGED, sa CI source #45046140595 SUCCESS sur HEAD exact `dc09106bf1fdc87df2e1258b8e8398e580f3cb9a`; son nouveau postmain #45053850972 n'est pas réputé PASS avant vérification indépendante. PR #35 DRAFT conserve le HEAD historique `41ce7b915e76d22785d53d7fffe288d113dd0bf5`. Aucun ancien module chargé/exécuté ni donnée opérateur lue.

## Trois paires source/test examinées sans exécution

| Ancien module Python de #35 absent du main | Ancienne sémantique visible dans la source | Comparaison limitée avec `main` | Décision |
| --- | --- | --- | --- |
| `tools/m3_2_chronology_navigation_reference.py` (Stage 24, blob `5826f9c79532e11520e139637859b1d778f92e7f`) | `NavigationFilters` : sous-ensemble de statuts active/replaced/withdrawn, sous-ensemble de quatre temporalités, ID calendrier, ID source, recherche NFC/casefold des libellés ; `NavigationPage` découpe après filtrage, curseurs liés à un fingerprint snapshot+filtres+taille, taille max héritée | `src/M32ChronologyPreview.tsx` valide des projections fictives ; `src/M32ChronologyConsultation.tsx` expose une sélection sur ancres courantes. Aucune équivalence démontrée de la recherche Unicode, filtrage multistatuts ou curseur fingerprint | `REVIEW_ONLY_NOT_PORTED` |
| `tools/m3_2_chronology_comparison_reference.py` (Stage 25, blob `9f6dfd8d09cb4829b6b2ee168f0a1043212d1885`) | `compare_filtered_anchors` compare deux ID actifs du **même Univers** et visibles sous les mêmes filtres Stage24 ; relation `same/before/after/incomparable` selon précédences, ni ordre de manuscrit ni ordre de révélation déduits | `src/M32WorldOrderComparison.tsx` calcule des témoins fictifs sur projection actuelle. Existence de noms similaires n'établit pas la même validation de filtrage ni la parité avec l'ancien modèle de snapshot | `REVIEW_ONLY_NOT_PORTED` |
| `tools/m3_2_chronology_selection_review_reference.py` (Stage 29, blob `a6985f28f1f91cd4afc415469ef59c11f867c5c4`) | `review_selected_witness` revalide deux sélections explicites sur pages filtrées, restitue positions absolues et locales, curseur de navigation, et `WitnessConsultationPage` avec pagination propre ; refus d'un témoin incohérent | `src/M32ChronologyConsultation.tsx` offre une consultation fictive mais pas de preuve d'équivalence des localisateurs interpages et témoins paginés de Stage29 | `REVIEW_ONLY_NOT_PORTED` |

## Tests historiques appariés — inventaire des signatures, sans exécution

Les sources des trois anciens fichiers de tests ont été lues par identifiant Git blob exact. Le comptage lexical porte uniquement sur les définitions Python `def test_*`, sans invocation de `unittest`, import ni évaluation d'assertion : 50+26+34 = **110 définitions nommées inspectées en source seulement**. **TOTAL_110_METHOD_NAMES_SOURCE_INSPECTED_NOT_EXECUTED**.

| Étape | Script Python absent | Test historique absent | Blob script | Blob test | Méthodes | Décision |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | `tools/m3_2_chronology_navigation_reference.py` | `tools/test_m3_2_chronology_navigation_reference.py` | `5826f9c79532e11520e139637859b1d778f92e7f` | `91fabd546a22fb8f98481f7f0b8cba85600a1490` | 50 | SOURCE_REVIEW_ONLY_NOT_EXECUTED |
| 25 | `tools/m3_2_chronology_comparison_reference.py` | `tools/test_m3_2_chronology_comparison_reference.py` | `9f6dfd8d09cb4829b6b2ee168f0a1043212d1885` | `6488ec2fdec95566358e48d0c6ef1ddbb5d7fad7` | 26 | SOURCE_REVIEW_ONLY_NOT_EXECUTED |
| 29 | `tools/m3_2_chronology_selection_review_reference.py` | `tools/test_m3_2_chronology_selection_review_reference.py` | `a6985f28f1f91cd4afc415469ef59c11f867c5c4` | `86dac0ab3aa3ae3fe524c2d77a406fd1852d2160` | 34 | SOURCE_REVIEW_ONLY_NOT_EXECUTED |

Exemples attestés **par nom de test uniquement** : Stage24 `test_equivalent_unicode_queries_still_have_distinct_cursors`, `test_cursor_refuses_same_filter_but_changed_snapshot`, `test_filter_multiple_statuses` ; Stage25 `test_replaced_historical_anchor_refused`, `test_result_independent_of_pagination_width` ; Stage29 `test_changed_witness_page_width_invalidates_old_cursor`, `test_navigation_cursor_stale_on_snapshot_change`, `test_large_navigation_across_more_than_512_anchors`. La couverture, les résultats PASS/FAIL, l'équivalence moderne et l'acceptation restent **NON QUALIFIÉS**.

Ces trois modules ont leurs tests appariés historiques `tools/test_m3_2_chronology_navigation_reference.py`, `tools/test_m3_2_chronology_comparison_reference.py` et `tools/test_m3_2_chronology_selection_review_reference.py`. **La source des trois outils et les signatures des trois tests appariés sont inspectées** ; aucun test historique n'a été exécuté, ses assertions n'ont pas été vérifiées et aucune équivalence moderne n'est admise. Le présent rapport n'affirme pas qu'une fonction React actuelle remplace une API Python donnée. Les dépendances de ces anciens modules à `m3_2_supersession_reference.py`, projection, pagination et consultation des témoins rendent toute importation isolée non justifiée.

Avec ces trois paires, **5 des 20 paires** ont une *description sémantique partielle* (deux Stage 21/23 dans `M3_2_PR35_TWENTY_PYTHON_PAIRS_SCOPE_20261122.md` + trois présentes), et **15 restent inventoriées seulement nominalement**. Ce décompte est un avancement de revue **et non une équivalence, un portage, une couverture de test acceptée ou une clôture**.

## Décision et prochaines preuves

Décision : `NO_SEMANTIC_EQUIVALENCE`, `NO_AUTO_PORT`, `NO_RUNTIME_ADMISSION`. M32-007 [ ] et M32-050 [ ] restent `OPEN_NOT_ACCEPTED`. Pour chaque paire, une décision ultérieure requiert revue du test historique, délimitation des dépendances, identification du besoin produit sur base moderne, éventuelle implémentation ciblée **dans un atelier source-only**, puis CI Windows au HEAD exact et postmain indépendant. Aucun module historique, `lib.rs`, `App.tsx`, runtime, SQLite, WAL/SHM, IPC, sauvegarde, migration ou writer n'est modifié ou exécuté ici.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45% indicatif) ; `PRODUCT_FIRST_PARALLEL_SAFETY` ; checklist 104 : 13 CLOSED_SCOPED /91 OPEN_NOT_ACCEPTED. PR #35/#215 DRAFT NON ADMISES.

STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5, D3b-5 STOP ; live main/WAL/SHM et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
