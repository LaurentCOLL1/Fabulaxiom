# M3.2 — Stage 21 : projection de chronologie en lecture seule (synthétique)

**Statut : prototype Python indépendant, sur des objets en mémoire. Aucun accès SQLite, aucune application Tauri, aucune mutation locale, aucune interface React et aucune autorisation M3.2.**

## Autorité vérifiée

- Prédécesseur exact : branche PR #35 `a1c27c36fa5f48557ec1475fccf13577979d8d07`, Windows `pull_request` CI #38579592096 **completed/success 32/32**, incluant 25 tests de rectification Stage 20a. `main=f7eabfea74480d307b52d4b053730021efc95352` inchangée.
- `docs/qualification/M3_2_MANUAL_CHRONOLOGY_UX_CONTRACT.md` interdit de fusionner les dimensions « chronologie du monde », « ordre narratif » et « révélation lecteur ».
- Le simulateur `tools/m3_2_supersession_reference.py` conserve les anciennes assertions, interdit les mutations silencieuses, les cycles historiques et la correction d'ancres reliées par des précédences préexistantes.
- Le schéma v7 M3.1 candidat interdit UPDATE/DELETE des calendriers, ancres et précédences ; `world_time_precedences_guard` recherche les cycles dans **tout l'historique**, pas dans une sous-vue active.
- L'audit physique réel Stage 18.1 v7 isolé a réussi, mais la qualification globale demeure **PENDING_EXTERNAL_ATTESTATION** (21 empreintes historiques, 3 observations récentes, 2 éléments non ancrés).

## Les quatre API conceptuelles, sans lecture de fichier

| API Python de référence | Contrat |
|---|---|
| `universe_view(snapshot, universe)` | Assertions d'un seul Univers, dans l'ordre d'insertion **d'affichage uniquement**, sans prétendre les classer dans le temps |
| `inspect_anchor(snapshot, universe, id)` | Statut `active`, `replaced` ou `withdrawn` ; conserve la valeur d'origine, le prochain ID et la raison |
| `lineage(snapshot, universe, origin_id)` | IDs successifs, IDs des événements et raisons humaines en chaîne ; arrêt actif ou retiré |
| `relative_world_order(snapshot, universe, left_id, right_id)` | Résultat `same`, `before`, `after` ou `incomparable`, **uniquement** par transitivité des relations explicitement saisies |

L'API de comparaison refuse toute ancre remplacée ou retirée, plutôt que de lui attribuer automatiquement la date de son successeur. Les deux IDs doivent être actifs dans le même Univers ; sinon le résultat est un refus déterministe. Les chaînes de corrections peuvent être consultées pour l'historique, mais ne réécrivent jamais l'ancre initiale. Les dates en calendrier fictif, leurs étiquettes brutes, les précisions approximatives et les IDs de révision restent inchangés ; aucun `Date.parse` / Unix epoch / calendrier grégorien n'est introduit.

`UniverseView` porte explicitement `narration_order_available=false`, `reader_reveal_order_available=false`, `chronology_editing_authorized=false`. Il ne s'agit pas d'une décision future permanente pour l'ordre narratif existant : le *modèle synthétique Stage 21*, isolé des romans et chapitres, ne dispose pas de ces informations. Il ne prétend donc pas les fabriquer.

## Garanties, tests et restrictions

- `tools/m3_2_chronology_projection_reference.py` importe seulement le modèle synthétique Stage 20. Les types de sortie sont des `dataclass(frozen=True)`, la lecture ne construit aucune nouvelle assertion et ne modifie pas les anciens tuples.
- `tools/test_m3_2_chronology_projection_reference.py` comporte **25 nouveaux tests** : Univers multiples et absence de fuite transversale, ordre d'affichage non temporel, panneaux non disponibles, calendriers fictifs séparés, comparabilité transitivement démontrée, non-comparabilité des ancres sans lien, inspection historisée, lignée multi-rectifications avec raisons, rétractation, refus d'ancre non active, préservation des IDs de révisions, immutabilité du snapshot et absence d'ordre fabriqué.
- Tous les tests sont déterministes et ne créent ni base de données, ni fichier de sauvegarde, ni répertoire opérateur. La nouvelle étape CI Windows exécute ces 25 tests **en plus** des 25 tests Stage 20a et des 33 tests de provenance. Elle ne transfère jamais la qualification de l'ancien SHA à un nouveau HEAD.
- L'intégrité des vrais triggers SQLite, des jointures vers la révision et des transactions Rust reste à qualifier séparément après attestation externe. Les fonctions Python **ne sont pas** une implémentation de l'interface M3.2.

## Interdictions inchangées

Ne pas créer un huitième worktree et ne pas modifier les sept déjà présents. Ne pas ouvrir ni migrer la production SQLite v6 ou la copie historique M3.1 v7. Ne pas modifier les archives ACL, les signatures ou les sauvegardes. Ne pas créer de nouvel identifiant d'application, d'IPC d'écriture, de migration 007 automatique ou de mécanisme de résolution rétroactive des preuves. La PR #35 reste DRAFT/non fusionnée ; M3.3 est bloqué.

Documentation SQLite indépendante : https://www.sqlite.org/lang_createtrigger.html et https://www.sqlite.org/lang_with.html .
