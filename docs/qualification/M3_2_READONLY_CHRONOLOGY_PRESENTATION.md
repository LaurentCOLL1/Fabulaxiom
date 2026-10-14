# M3.2 — Stage 22 : contrat de présentation de chronologie en lecture seule

**Prototype Python purement synthétique, non branché sur React, Rust/Tauri ou SQLite. Aucune migration, écriture, sauvegarde ou commande opérateur.**

## Autorité et limites
Le Stage 21 à SHA `3bd899cc5876042ff57c3b8ab63fb91a6a40a2c9` a obtenu la CI Windows exacte [#38595478362](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/38595478362) **completed/success 33/33**, comprenant les 25 tests de projection Stage 21, 25 tests de supersession Stage 20a, 33 tests de revendication de provenance Stage 19.1b, et les contrôles Rust/React précédents. `main=f7eabfea74480d307b52d4b053730021efc95352` inchangée, PR #35 ouverte DRAFT et non fusionnée.

Le réel contrôle Stage 18.1 sur la **copie SQLite v7 M3.1 isolée** a réussi uniquement en lecture seule : empreinte avant/après identique, intégrité/FK/schéma et digest historique v6, 26 rôles vérifiés. Cela n'autorise aucune écriture M3.2. L'autorité externe est **PENDING_EXTERNAL_ATTESTATION** : 21 pins SHA historiquement ancrés, 3 observations récentes et 2 rôles non ancrés. Aucun témoin historique nouveau n'a été authentifié.

## DTO stable pour une interface future, pas une interface réelle

`tools/m3_2_chronology_presentation_reference.py` reçoit seulement un `SyntheticSnapshot` Stage 20/21 en mémoire. Il calcule un `ChronologyReadPanel` immuable comprenant :
- `universe_id`, `data_origin=synthetic_in_memory_reference_only`, `display_order_semantics=source_insertion_order_not_world_time`.
- Les `AnchorCard` de cet Univers uniquement, avec ID d'assertion, `time_kind`, calendrier fictif, étiquette brute, fenêtre littérale, précision, ID immuable de révision, état `active/replaced/withdrawn`, ID successeur, raison, IDs et raisons de la lignée complète.
- Les `OrderComparison` sur paires **explicitement demandées**, avec `same/before/after/incomparable` uniquement par les précédences humaines transitives déjà qualifiées Stage 21.
- Les états `narration_order=not_available_in_synthetic_projection`, `reader_reveal_order=not_available_in_synthetic_projection` et `edit_controls_available=false`.

L'ordre d'insertion ne doit **jamais être affiché comme chronologie prouvée**. Deux dates littérales (« première cloche », « troisième cloche »), y compris d'un même calendrier fictif, ne justifient aucune conversion numérique ni relation avant/après. Une assertion remplacée ou retirée n'est pas comparable comme assertion courante ; elle demeure consultable historiquement. Aucune étiquette, ID de révision ou source n'est automatiquement substitué.

`presentation_json` rend une chaîne JSON à clés déterministes, exclusivement à partir du DTO immuable. Ce mécanisme n'effectue **aucun appel réseau, aucune écriture disque ni IPC**. Après désérialisation, un consommateur doit néanmoins appliquer ses propres contrôles d'affichage et d'échappement ; cette chaîne n'est pas un mécanisme de transfert applicatif activé.

## Limites de volume et de sécurité
Le prototype refuse plus de **512 ancres visibles d'un Univers** ou **128 paires de comparaison demandées**, les paires dupliquées et les formes incorrectes. Toute paire doit rester active et appartenir à l'Univers demandé ; une requête hors Univers refuse plutôt que divulguer des données. Ces limites sont de conception synthétique, non des paramètres de pagination ou de performance UI qualifiés pour une production.

Les `dataclass(frozen=True)` n'autorisent pas la réaffectation des champs, mais cela n'est **pas une garantie cryptographique**, ni une preuve de sécurité de l'interface. L'existence réelle d'une révision, le type de l'entité `event`, les jointures de l'Univers et les contraintes transactionnelles exigeraient des vérifications Rust/SQLite distinctes, interdite ici.

## Qualification synthétique Stage 22
`tools/test_m3_2_chronology_presentation_reference.py` ajoute **25 tests Windows synthétiques**, sans connexion SQLite ni chargement de données opérateur : cloisonnement par Univers, préservation de l'ordre d'affichage, rectification et retrait, lignée avec raisons, comparaison explicite/incomparable, absence de conversion de calendrier, conservation de la révision source, contrôles UI faussement disponibles, limites 512/128, veto des paires fausses ou dupliquées, JSON déterministe et données en mémoire inchangées. Un nouveau workflow exact-head devra passer **34 étapes**, dont 25 Stage22, 25 Stage21, 25 Stage20 et 33 tests de provenance. L'ancien résultat 33/33 qualifie uniquement le SHA précédent.

## Interdictions inchangées
Conserver les sept worktrees Windows d'origine, la production restaurée M1.5 SQLite v6, la copie M3.1 v7 isolée, les backups et les archives ACL. Aucun huitième worktree, aucune nouvelle identité d'application, aucune migration normale 007, aucun IPC d'écriture, aucune modification de tables v7 immuables, aucune fusion de PR #35, aucun M3.3. Le prototype ne remplace pas les attestations historiques externes.
