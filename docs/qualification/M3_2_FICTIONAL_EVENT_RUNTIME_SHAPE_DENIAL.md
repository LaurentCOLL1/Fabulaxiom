# M3.2 — refus déterministe de faux enregistrements d'événements fictifs

**23 octobre 2026 — candidature strictement source-only, RAM inventée, aucune entrée dans Tauri/App.tsx.**

## Lacune et comportement

Les types TypeScript sont effacés à l'exécution. Jusqu'à la PR #149, une version d'événement `null` ou un `event_id` numérique introduits par un appelant non typé pouvaient déclencher un `TypeError` brut lors du parcours du carnet fictif, tandis qu'un tableau enrichi de propriétés pouvait imiter un événement ou un audit. Cela ne donne aucune preuve de source fiable ; le bon comportement est un **refus métier explicite**.

Le validateur vérifie maintenant la forme objet (non-tableau) du carnet, de chaque entrée `events` et de chaque audit, ainsi que le type chaîne des identifiants événement/univers avant d'appliquer les invariants déjà qualifiés (versions, ordre, actions, retraits et compteurs). Neuf tests Vitest #33–41 couvrent `null`, primitifs, identifiant absent ou numérique, tableaux mimétiques et mutation depuis un carnet mal formé, puis un parcours valide création/correction/retrait intercalé. Ce contrôle ne répare ni ne reconstruit de données.

## Checkpoint historique distinct

PR [#149](https://github.com/LaurentCOLL1/Fabulaxiom/pull/149) source `6c040d264035bf1c92d256b58459382b5d7faa10`, [CI #39994596525](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39994596525) terminal SUCCESS ; fusion protégée `main=77e253193cae3d29ae164875c65be1bf3186f4ad`, [CI postmain #39996127567](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/39996127567) terminal SUCCESS. Chacune : 76 étapes Windows, 84 tests de continuité, 32 tests d'événements inventés, 62/62 Chromium fictif par mode et 132 tests Rust principaux. Première CI #39994287773 FAILURE sur SHA antérieur préservée dans l'issue #38, non réutilisée.

**Pour cette nouvelle PR :** exiger une nouvelle CI terminale au HEAD final (85 contrats, 41 tests du carnet, 62/62 Chromium par mode, Rust), vérification diff/reviews/threads et `Protect main`, puis uniquement fusion protégée `expected_head_sha`; vérifier postmain séparément.

**STOP réels inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, source `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucune SQLite originale v6/v7, sauvegarde, ACL, WAL, marqueur, migration 007, IPC writer, M3.3, ComfyUI, release ni Windows opérateur. La cohérence structurelle ne constitue pas une provenance certifiée.
