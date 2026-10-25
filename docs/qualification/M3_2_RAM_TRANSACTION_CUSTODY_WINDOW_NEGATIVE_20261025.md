# M3.2 — Fenêtre transactionnelle RAM vs contrôle rétrospectif, 25 octobre 2026

**Seulement deux tests Rust de laboratoire sur base `mode=memory` inventée ; jamais une procédure opérateur, jamais un original, jamais un G3 réel.**

## Checkpoint GitHub exact et preuve déjà acquise

Après la [PR #174](https://github.com/LaurentCOLL1/Fabulaxiom/pull/174), source `a9a031e3f7322e39475c70c2a1111fdc0c37f047` ([CI source #40199121197](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40199121197) SUCCESS), fusion protégée `main=0c1aee574832a3f48571546b345ebaad9228c163`, [CI postmain #40200127549](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40200127549) SUCCESS indépendante sur ce SHA. Les 81 étapes Windows, 108 contrats de continuité, 96 Vitest fictifs, Chromium 82/82 chacun des modes normal / CSP strict, 132 Rust de base, et `toy_16`–`toy_19` sous feature test-only ont réussi. [Issue #38 terminale](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6399200030). Ces observations n'identifient pas de source originale et ne certifient pas l'absence d'écrivain.

## Deux cas nouveaux à vérifier réellement dans GitHub CI

Uniquement `#[cfg(test)]`, feature `m32-g3-owned-ram-toy`, au sein de `src-tauri/src/m32_preopened_query_only_toy.rs`. Les deux connexions réutilisent la fabrique existante `invented_shared_ram_pair` et une URI `file:m32-invented-foreign-writer-<id>?mode=memory&cache=shared`, distincte par test et sans fichier disque ni identité privée.

- **`toy_20_data_version_postflight_is_not_a_future_write_barrier`** : après un `VersionedFictionalReader::read_again()` accepté, un écrivain fictif distinct effectue volontairement un `UPDATE` **après le dernier contrôle**. Le résultat déjà rendu ne peut pas être transformé rétroactivement en verrou ou attestation ; une lecture suivante voit la variation de `data_version` et rejette. Le scénario est déterministe, sans temporisation ni race aléatoire.
- **`toy_21_shared_ram_read_transaction_holds_lock_only_until_release`** : le lecteur ouvre `BEGIN DEFERRED TRANSACTION` et exécute un `SELECT`, tenant un verrou de table **dans ce mode SQLite shared-cache en mémoire seulement**. Le second handle tente un `UPDATE` et reçoit un refus ; le lecteur observe encore l'ancienne valeur. Après `ROLLBACK` **uniquement de la transaction RAM inventée**, l'UPDATE tierce réussit. Ce verrou cesse à la libération ; aucune absence continue d'écrivain ou garantie de conservation d'une base réelle n'en découle.

Ces scénarios ne remplacent pas la vraie voie G3 : authenticité et provenance source, identifiants Windows et ancêtres conservés, journaux WAL/rollback/hot journal, OS/IPC, écriture par d'autres processus, isolation d'une acquisition ni préservation du support réel restent inconnus. `PRAGMA data_version` est un signal d'invalidation postérieure, pas un verrou ; la transaction en cache partagé ne généralise pas un protocole de verrouillage fiable sous d'autres modes SQLite.

**Docs de référence** : [SQLite PRAGMA data_version](https://www.sqlite.org/pragma.html#pragma_data_version), [SQLite shared-cache memory transactions](https://www.sqlite.org/sharedcache.html), [SQLite transaction isolation](https://www.sqlite.org/isolation.html), [SQLite Online Backup](https://www.sqlite.org/backup.html).

## Discipline de source et sécurité

Aucun nouveau `Connection::open` ou `open_with_flags`, aucune modification des sites d'ouverture approuvés dans l'inventaire Rust SQLite, pas de fichier source propre à l'opérateur ni SQL de production, pas de migration 007, IPC writer, backup, lecture ACL, sidecar, marqueur ou Windows. Contrat de continuité #109 pour conserver la limite. Demander CI source complète terminale au SHA exact et, après fusion protégée, CI postmain indépendante avant enregistrement terminal append-only dans l'issue #38.

**STOP constants** : G2A `PASS_METADATA_ONLY_OWNER_REPORTED`, B0/B1 `OBSERVED_PARTIAL_ONLY_OWNER_REPORTED`, G2B `NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, `SQLITE_WRITER_ABSENCE=NOT_PROVEN`, G2C `NOT_AUTHORIZED`, réel G3 `STOP_UNAVAILABLE`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT, GLib Linux `OPEN_NOT_REMEDIATED`.

**PAS UNE ACCEPTATION M3.2 / G2B / G3. Test-only et aucune autorisation nouvelle.**
