# M3.2 — Lecture sale et rollback invisibles au `data_version` (RAM imaginaire)

**25 octobre 2026 · SOURCE-ONLY · SYNTHETIC_TEST_ONLY · CANDIDAT, jamais résultat d'opérateur.**

## Base vérifiée et point d'arrêt

La [PR #176](https://github.com/LaurentCOLL1/Fabulaxiom/pull/176), HEAD source exact `8b889049c118d7a8dcea21b5ce77a6bd2ce2b278`, [CI #40212798456](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40212798456) `completed/SUCCESS` (81/81 Windows ; 110 contrats ; 96 Vitest inventés ; Chromium 82/82 en deux modes ; 132 Rust de base ; `toy_22`/`toy_23` PASS), est fusionnée par squash protégé sur `main=254384336d8c086fefec769c41cb7723112c9077`. La [CI postmain indépendante #40213790809](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40213790809) est `completed/SUCCESS` (80 SUCCESS, 1 SKIPPED attendu). Premier essai source #40212633142 : FAILURE sur un SHA différent, non transférable. [Observation append-only issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6400559530).

`toy_22` a borné le verrou de lecture à une seule table shared-cache, `toy_23` a montré l'absence de ce verrou sous `read_uncommitted=ON`. Ils ne constituent ni une preuve de quiescence, ni une qualification de source réelle.

## Nouvelles expériences strictement inventées

- `toy_24_read_uncommitted_sees_uncommitted_value_then_rollback` : deux connexions partageant exclusivement une base `file:m32-invented-foreign-writer-<id>?mode=memory&cache=shared` créée dans le test. Le lecteur `PRAGMA read_uncommitted=ON` voit une description **non commitée** écrite par l'autre connexion pendant `BEGIN IMMEDIATE TRANSACTION`. Le writer exécute `ROLLBACK` ; le lecteur retrouve la valeur initiale. `PRAGMA data_version` reste égal à la mesure initiale **avant, pendant et après** l'annulation.
- `toy_25_read_uncommitted_observes_rolled_back_cardinality` : même modèle RAM fictif, insertion de la ligne inventée 2 non validée, cardinalité temporaire de 1 à 2, `ROLLBACK` puis retour à 1 ; `data_version` du lecteur reste identique aux trois instants.

Les deux assertions négatives illustrent qu'une observation sale peut ne correspondre à **aucun état jamais validé** ; le test d'un compteur de commits ne convertit pas cette observation en preuve d'absence d'écrivain. Aucune mesure, attestation, existence de writer, copie ou transaction de Windows opérateur n'est inférée.

Références primaires : [SQLite, isolation et lectures sales en shared-cache](https://www.sqlite.org/isolation.html) ; [SQLite, shared-cache et read_uncommitted](https://www.sqlite.org/sharedcache.html#read_uncommitted_isolation_mode) ; [SQLite, `PRAGMA data_version`](https://www.sqlite.org/pragma.html#pragma_data_version). SQLite déconseille shared-cache pour les applications modernes ; il sert ici uniquement de contre-exemple contrôlé et ne se transfère pas au cas réel.

## Décision conservatrice

**Candidate, sans PASS anticipé.** Les seuls ajouts autorisés sont deux tests Rust de feature et les documents/contrats source-only. Pas de SQLite originale v6/v7, backup, ACL, journaux, marqueur, migration 007, IPC writer, Windows opérateur ou autorisation implicite. G2B `NOT_ACCEPTED` ; absence d'écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 `OPEN/DRAFT`. Les futurs résultats source et postmain exigent SHA exact, CI terminale indépendante, diff/reviews/threads, puis checkpoint append-only issue #38.
