# M3.2 — Double échantillon stable mais jamais validé (SQLite RAM imaginaire)

**25 octobre 2026 · CANDIDAT SOURCE-ONLY · SYNTHETIC_TEST_ONLY · aucune exécution sur Windows opérateur.**

## Checkpoint exact préalable

[PR #177](https://github.com/LaurentCOLL1/Fabulaxiom/pull/177) HEAD source `32093f7f31f26c98e7b91bc9d25930ee4f973d27` : [CI source #40219228723](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40219228723) `completed/SUCCESS` (81 étapes Windows). Squash protégé `main=c1868256739247810ecf6b606e051b53b8c0d529`, [CI postmain indépendante #40220215000](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40220215000) `push/completed/SUCCESS` (80 SUCCESS et 1 SKIPPED attendu). Les deux journaux confirment **111 contrats**, **96 Vitest fictifs**, Chromium **82/82** normal et CSP stricte, **132 Rust de base**, `toy_24`/`toy_25` PASS. [Commentaire terminal issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6401436944). Ces résultats ne se transfèrent jamais à un HEAD suivant.

## Contre-exemple proposé (un seul test Rust)

`toy_26_repeated_dirty_read_stable_guards_do_not_prove_commit` crée deux connexions à une SQLite `mode=memory&cache=shared` de nom unique et entièrement inventée. Le lecteur conserve `PRAGMA query_only=ON`, active `PRAGMA read_uncommitted=ON` et relève `total_changes()` et `PRAGMA data_version` sur **sa propre connexion**. L'autre connexion exécute `BEGIN IMMEDIATE TRANSACTION` et modifie une description fictive, sans `COMMIT`.

Le lecteur observe **deux fois exactement la même valeur non commitée** ; avant, pendant chaque lecture et après l'annulation, ses compteurs `total_changes()` et `data_version` restent inchangés. Après `ROLLBACK` de l'autre connexion, la description originale réapparaît : les deux lectures identiques ne correspondaient à **aucun état durablement validé**. `query_only` ne prouve que la restriction d'écriture locale de ce lecteur, et aucune de ces observations n'atteste l'absence d'écrivain tiers.

Un pré-test Python `sqlite3` sur une RAM jetable et sans fichier a reproduit `('invented dirty', 1, 1)` deux fois avant `ROLLBACK` puis `'original'`. Ceci prépare le test CI Rust, mais **ne vaut ni PASS CI anticipé ni qualification externe**.

Références primaires : [SQLite : isolation et lectures sales shared-cache](https://www.sqlite.org/isolation.html), [SQLite : `read_uncommitted` shared-cache](https://www.sqlite.org/sharedcache.html#read_uncommitted_isolation_mode), [SQLite : `PRAGMA data_version` indique les commits tiers](https://www.sqlite.org/pragma.html#pragma_data_version). SQLite déconseille shared-cache pour les nouveaux développements ; c'est ici une limite expérimentale, pas une stratégie G2C/G3.

## STOP intangibles

Aucune ouverture de SQLite v6/v7 originale, aucun backup, ACL, journal, marqueur, migration 007, IPC writer, runtime Tauri ou action Windows opérateur. G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 `OPEN/DRAFT`. Les CI source puis postmain exigent deux SHA exacts et deux conclusions terminales ; diff, reviews, threads, ruleset `Protect main` et issue #38 append-only demeurent obligatoires.
