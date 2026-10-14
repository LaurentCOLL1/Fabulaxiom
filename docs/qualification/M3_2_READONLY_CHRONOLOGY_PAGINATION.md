# M3.2 — Stage 23 : pagination chronologique synthétique en lecture seule

**DESIGN ET TESTS SYNTHÉTIQUES EXCLUSIVEMENT. Aucune interface React, aucun IPC Rust/Tauri, aucune connexion SQLite, aucune écriture, aucun worktree opérateur supplémentaire.**

## Prédécesseur et autorités
- La branche de la PR #35, au SHA pré-Stage23 `4f291197adc9017310342e6af38000f6d5a920c7`, a obtenu la CI Windows pull_request exacte [#38599527966](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38599527966), terminale **completed/success avec 34/34 étapes**, incluant 25 tests Stage22, 25 Stage21, 25 Stage20a et 33 tests de provenance.
- La branche protégée `main=f7eabfea74480d307b52d4b053730021efc95352` n'était pas modifiée ; PR #35 toujours OPEN/DRAFT.
- Stage22 : `present_chronology` refuse intentionnellement au-delà de 512 ancres affichées par Univers ; ce seuil ne prouve pas une limite fonctionnelle souhaitable pour les romans volumineux.
- L'audit physique réel Stage18.1 de l'unique copie M3.1 v7 isolée est qualifié en **lecture seule**. La décision globale reste `PENDING_EXTERNAL_ATTESTATION` : 21 empreintes historiquement ancrées, 3 observations contemporaines, 2 rôles non ancrés. Aucune attestation externe historique nouvelle n'a été vérifiée.

## Contrat strictement in-memory

Le nouveau module `tools/m3_2_chronology_pagination_reference.py` offre :
- `chronology_page(snapshot, universe, page_size=32, cursor=None)` : une page de 1 à **64** cartes `AnchorCard` déjà définies par Stage22, en préservant l'ordre d'insertion seulement **pour l'affichage**, sans tri temporel.
- `ChronologyPage` figé, avec `universe_id`, `anchors`, `next_cursor`, `display_order_semantics=source_insertion_order_not_world_time`, `edit_controls_available=false` et `data_origin=synthetic_in_memory_reference_only`.
- `chronology_page_json` : sérialisation déterministe de ce seul DTO. Aucun accès disque ou réseau.
- Lorsque la projection n'a pas d'ancre, la première page est vide et son curseur suivant vaut NULL. Une page terminale ne produit pas de curseur.

Les cartes montrent les ancres d'un seul Univers, toujours avec leur ID, calendrier fictif et libellé exact, révision historique immuable, statut `active/replaced/withdrawn`, raison et lignée entière des rectifications. Une correction ne retire pas l'ancienne ancre de ses pages historiques ; aucune ancienne source n'est réécrite. Les précédences humaines restent consultables via Stage21, sans créer d'ordre fictif en l'absence de liens.

## Curseur de cohérence, non de sécurité

Le curseur est une chaîne base64url de JSON contenant uniquement `v`, `u`, `fp`, `offset`. Sa version est 1 ; `fp` est une empreinte SHA-256 calculée sur la représentation en mémoire du **snapshot synthétique complet**, utilisée uniquement pour repérer une modification entre pages. Les contrôles refusent :
- ancien curseur sur snapshot modifié (même si le changement est dans un autre Univers — refus conservateur) ;
- curseur d'un autre Univers, version inconnue, offset négatif/hors plage, offset booléen, champs inattendus ;
- encodage invalide, clé JSON dupliquée, entrée non finie ou taille supérieure à **4096 caractères** ;
- taille de page incorrecte, nulle, booléenne ou supérieure à 64.

**Le curseur ne signe rien et ne vérifie aucune permission.** Un acteur connaissant le snapshot pourrait créer un curseur similaire. Il ne doit **jamais** être utilisé comme jeton d'authentification ou comme contrôle d'accès d'une API. La véritable application devrait appliquer des règles Rust/SQLite d'autorisation et d'isolation indépendantes. `repr(snapshot)` n'est pas un format interopérable garanti et ne constitue pas une empreinte d'archive.

## Suite d'acceptation synthétique

`tools/test_m3_2_chronology_pagination_reference.py` ajoute **28 nouveaux tests Windows** : parcours exact de 513 ancres sans doublon ni perte, résultats conformes aux cartes Stage22 pour un petit jeu, refus des curseurs obsolètes/hors Univers/modifiés, maintien des chaînes de correction et des retraits, préservation des fenêtres et des calendriers fictifs, refus des tailles et encodages invalides, déterminisme JSON, immutabilité des snapshots et interdiction du mode édition. La nouvelle étape CI doit passer avec toutes les anciennes suites ; la réussite du SHA précédent ne se transfère pas à ce nouveau code.

Les limites 64/4096 sont celles du **simulateur**, pas un engagement de conception définitif pour la future interface. Aucune mesure de performance ou sécurité en production n'est revendiquée.

## Portes inchangées

Les sept worktrees opérateur et les sauvegardes d'origine, les ACL, la production SQLite v6 restaurée et la copie M3.1 v7 isolée demeurent inchangés. Ne pas créer une huitième source locale ni une identité M3.2, ne pas activer la migration 007 au démarrage normal, ne pas ajouter de writer IPC ou de commandes de rectification, ne pas fusionner la PR #35 et ne pas passer à M3.3 tant que les attestations externes indépendantes manquent.

Référence langage Python : https://docs.python.org/3.12/library/dataclasses.html (les dataclasses `frozen=True` simulent l'immuabilité, sans fournir une garantie de sécurité cryptographique).
