# M3.2 — Lecture d'une connexion déjà ouverte, exclusivement en RAM fictive

**RUST TEST-ONLY, NON EXÉCUTABLE PAR L'OPÉRATEUR, NON AUTORISÉ G3.** Checkpoint du 20 octobre 2026 après fusion PR #94 sur `main=632e6d6d985affa6989bb220ddec99911e6ba1e6`. Re-fetch requis avant toute autre action.

## Objectif précis

Les tranches précédentes prouvent que les méthodes de statut et de sauvegarde de production utilisent `open_database`, qui peut créer/migrer une base. Cette expérimentation n'appelle **jamais** cette ouverture sur source. Elle accepte une **référence empruntée `&Connection` déjà ouverte**, et exclusivement une base imaginaire en mémoire privée créée dans la fixture de test.

`src-tauri/src/m32_preopened_query_only_toy.rs` définit `PreopenedFictionalReader<'a>` : constructeur sans paramètre chemin, version fictive 6 ou 7, validation de `PRAGMA database_list` (seulement main/temp, chemins vides), `PRAGMA query_only=ON` exigé **mais activé séparément dans la fixture**, présence exacte des versions imaginaires, contrôle logique d'intégrité/clé étrangère et `total_changes()` stable pendant la durée de l'emprunt. Toute anomalie renvoie une erreur de test.

**Important :** le simple fait d'emprunter `&Connection` et de constater `query_only=ON` ne rend PAS une connexion à un fichier réel sûre, ne verrouille pas un autre écrivain et ne prouve ni la provenance ni l'état des sidecars. `total_changes()` ne mesure que les changements de **cette connexion** ; il ne détecte pas les writes d'autres processus. L'invariant de fichier RAM et l'environnement fictif sont indispensables aux tests, non transposables automatiquement.

## Séparation compile/test

- Le fichier est référencé dans `src-tauri/src/lib.rs` uniquement sous `#[cfg(all(test, feature = "m32-g3-owned-ram-toy"))]`.
- Le feature `m32-g3-owned-ram-toy` est non défaut et déjà protégé par un `compile_error!` hors de `cfg(test)`. Aucune nouvelle commande Tauri, aucun IPC writer, aucun branchement dans l'exécutable normal.
- La seule `Connection::open_in_memory()` est dans le constructeur **du jeu de données inventé**, pas dans l'API de lecture. Ce constructeur exécute un schéma entièrement fictif, sans aucune migration applicative réelle ni disque.
- La CI utilise `cargo test --locked --features m32-g3-owned-ram-toy --lib m32_preopened_query_only_toy -- --nocapture` ; aucune commande locale à copier.

## Les 13 scénarios de tests

1. Lecture du schéma imaginaire v6 sans migration ni nouveau changement.
2. Lecture du schéma imaginaire v7.
3. Version attendue incohérente : refus.
4. Version inconnue : refus.
5. Connexion sans `query_only` : refus.
6. INSERT sous `query_only` : refus.
7. UPDATE et DROP sous `query_only` : refus.
8. Base RAM ATTACHée sous un autre schéma : refus.
9. Ligne de version manquante : refus.
10. Modification du contenu après qualification : emprunt invalidé.
11. Désactivation de `query_only` après qualification : refus.
12. Version fictive 0 non prévue : refus.
13. ATTACH post-qualification : refus.

## Ce que la CI ne prouve pas

Ce module ne valide ni les propriétaires réels sur Windows ni l'identité du fichier, ne garantit pas qu'un fichier WAL en lecture seule n'entraîne pas de création de `-wal` ou `-shm`, ne prouve pas de quiescence d'autres connexions, n'est pas une analyse concurrente atomique et ne donne aucun droit d'accès aux bases originales. Les tests observant `query_only` ne sont pas une alternative au protocole complet de provenance/exclusivité/journaux.

SQLite prévient que l'option `immutable=1` désactive le verrouillage et peut rendre les résultats incorrects si le fichier est modifié. Ce toy n'utilise pas `immutable=1`, ni `nolock=1`, ni l'API d'ouverture d'une base privée.

**Décisions inchangées :** `G2A=PASS_METADATA_ONLY_OWNER_REPORTED`, `PROCESS_WRITER_ABSENCE=NOT_PROVEN`, `REAL_G3=STOP_UNAVAILABLE`, `G2B/C/D/G3/G4/G5/G6=NOT_AUTHORIZED`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Aucun accès v6 production/v7 isolée, sidecars, WAL, backups, ACL, marqueur d'activation ; pas de migration 007, writer IPC, fusion PR #35, M3.3 ou release. Le consentement à l'unique G2-A est consommé.

Sources : https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html ; https://www.sqlite.org/uri.html ; https://www.sqlite.org/wal.html .
