# Fabulaxiom M3.2 — `data_version` contre les commits tiers, expérience RAM (25 octobre 2026)

**STATUT : TESTS RUST SYNTHÉTIQUES UNIQUEMENT. AUCUNE QUALIFICATION G2B/G3 RÉELLE. AUCUN ACCÈS WINDOWS OPÉRATEUR.**

## Justification après la PR #173

[PR #173](https://github.com/LaurentCOLL1/Fabulaxiom/pull/173) fusionnée : SHA source `a44e9b946f1f420c44f1403f412fb59ccca9a284`, CI source [#40189597795](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40189597795) SUCCESS ; squash protégé `main=63faae23c63ae0012f74c63aad730d93f95ce1c2`, CI indépendante postmain [#40190429389](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40190429389) SUCCESS sur ce SHA exact, 81 étapes Windows, 107 contrats, 96 Vitest fictifs, Chromium 82/82 par mode, 132 tests Rust par défaut, nouveaux scénarios `toy_14` et `toy_15` PASS sous feature. [Checkpoint terminal #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6397363412). Aucun des tests n'ouvre SQLite d'origine ni ne l'authentifie.

Le témoin négatif `toy_14` démontre qu'une autre connexion SQLite peut valider un `UPDATE` de texte fictif dans la **même base en mémoire** alors que `query_only=ON` et `total_changes()` sont inchangés sur le lecteur et que la vérification faible accepte le même nombre de lignes. Cette faille doit rester visible dans les tests ; ne jamais la faire passer pour une autorisation G3.

## Nouvel incrément de vérification (CI seulement)

Ajouter uniquement dans le module existant `src-tauri/src/m32_preopened_query_only_toy.rs` (compilé uniquement `cfg(test)` + feature opt-in `m32-g3-owned-ram-toy`) un type `VersionedFictionalReader`. Il combine la validation faible conservée avec des **comparaisons de `PRAGMA data_version` sur la même connexion au début/à la fin** de chaque observation. Toute divergence entraîne `Error::InvalidQuery`, sans auto-réessai ni nouveaux accès.

Quatre expériences Rust réelles **sur valeurs inventées en RAM**, avec deux connexions sur `file:m32-invented-foreign-writer-<id>?mode=memory&cache=shared` :
- `toy_16` : un écrivain indépendant remplace un texte sans changer le nombre de lignes ; le contrôle faible `PASS`, la nouvelle garde `STOP`.
- `toy_17` : un écrivain remplace **puis restaure** le texte d'origine ; la simple comparaison du contenu au point final ou du compteur local serait insuffisante ; `data_version` incrémenté provoque `STOP`.
- `toy_18` : sans écritures tierces, l'observation est répétable et acceptée.
- `toy_19` : une écriture via la **même** connexion n'augmente pas nécessairement sa propre `data_version` ; le contrôle local `total_changes` doit toujours la refuser. Ceci prouve que les deux signaux sont complémentaires, pas interchangeables.

Le code n'ajoute **aucun `Connection::open` ou `open_with_flags`** au-delà des deux ouvertures RAM revues dans #173, aucun flag SQLite nouveau, aucun chemin disque, aucune dépendance, SQL de production, migration 007, sauvegarde, WAL, création de fichier, IPC, Tauri State ou commande opérateur. Inventaire source-only SQLite et refus des nouveaux sites de création doivent continuer de réussir **sans modification des compteurs autorisés**.

## Limites / STOP

`PRAGMA data_version` permet d'invalider **rétrospectivement** une observation après des commits tiers détectés par la connexion. Ce n'est **pas** un verrou, une observation atomique des octets, une barrière d'écriture pendant la lecture, une attestation de provenance, un identifiant Windows FileId continu ou une preuve qu'aucun autre processus écrit **maintenant ou après le dernier contrôle**. Les commits de la même connexion n'incrémentent pas ce signal. Deux lectures successives ne transforment pas l'ouverture d'une source non authentifiée en contrôle de garde valable. Les comparaisons de `data_version` issues de connexions différentes sont dépourvues de signification ; n'en jamais comparer entre elles.

**Sources officielles :** https://www.sqlite.org/pragma.html#pragma_data_version ; https://www.sqlite.org/c3ref/total_changes.html ; https://www.sqlite.org/backup.html . Aucun de ces textes n'autorise une lecture ou une capture de la source protégée.

**STOP invariants :** B0/B1 `OBSERVED_PARTIAL_ONLY_OWNER_REPORTED`, `G2B=NOT_ACCEPTED`, identité `PARTIAL_LOCAL_IDENTITY_ONLY`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, M3.2 `IN_PROGRESS_NOT_ACCEPTED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Route A propriétaire réel déjà ouvert `UNAVAILABLE_NOT_PROVEN`, route B source froide `NOT_PROVEN`, C développement fiction uniquement. Linux GLib `OPEN_NOT_REMEDIATED`.

**Qualification à établir, non présumée :** source-HEAD final, toutes les étapes Windows terminales vertes, contrat de continuité #108, quatre nouvelles expériences sous feature + les précédentes toujours vertes ; squash protégé `expected_head_sha`, puis CI postmain indépendante sur SHA fusionné et entrée append-only dans l'issue #38. Aucune mutation opérateur.
