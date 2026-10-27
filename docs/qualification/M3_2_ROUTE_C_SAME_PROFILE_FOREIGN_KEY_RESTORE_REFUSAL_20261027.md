# Voie C — restauration refusée pour incohérence logique SQLite dans le même profil (CI)

**27 octobre 2026 — CANDIDAT SOURCE/FIXTURES ; aucune réussite anticipée sur le nouveau SHA.**

## Autorité GitHub réactualisée

- [PR #187](https://github.com/LaurentCOLL1/Fabulaxiom/pull/187) **MERGED** : source `3029bf61d526a243a431bf2c151de0ebeaf50818`, [CI source #40444374426](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40444374426) `SUCCESS` ; squash sous `Protect main` `0b0964a723340fd832134691fdd93563c1afe9c0`, [CI postmain #40445392523](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40445392523) `SUCCESS` indépendamment. 141 Rust de base, 5/5 Greenfield, 7 gardes source, 117 contrats. [Issue #38 append-only](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6433265532).
- Le profil Windows de Laurent **`com.fabulaxiom.greenfield.v1` est déjà fonctionnel et reste unique**. La restauration crée un **fichier** SQLite neuf dans ce **même** profil, sans écraser l'ancien. Aucune création de nouveau profil Tauri n'est demandée.

## Nouvelle qualification négative

Le test Rust `greenfield_ci_same_profile_foreign_key_invalid_backup_cannot_replace_active_work` n'utilise qu'une racine temporaire jetable créée par le test. Il :

1. Crée un Univers dans une SQLite v6 neuve, produit une sauvegarde valide, puis poursuit le travail dans l'ancienne SQLite.
2. Restaure la sauvegarde valide vers un **nouveau fichier dans la même racine de test**, avec marqueur d'activation ; capture les octets de l'ancienne et de la nouvelle SQLite, le nom et le contenu du marqueur, la liste des fichiers et la sauvegarde saine.
3. Crée une **deuxième sauvegarde jetable**, ouvre uniquement cette copie, désactive ses clés étrangères et introduit un roman orphelin (`universe_id` absent). La structure des pages reste saine (`PRAGMA integrity_check = ok`), tandis que `PRAGMA foreign_key_check` relève l'incohérence.
4. Demande la restauration de la seule sauvegarde incohérente : le service doit renvoyer `integrity`, sans écrire de nouveau marqueur ni sélectionner d'autre fichier actif.
5. Vérifie que les noms de fichiers, les octets des deux SQLite et du marqueur restent identiques, que la sauvegarde saine et la sauvegarde incohérente ne sont pas modifiées, et que l'ancienne SQLite conserve les deux Univers contre un pour l'active.
6. Ne supprime que la racine temporaire **créée exclusivement par le test**.

Ce cas complète le refus de sauvegarde physiquement corrompue de la PR #187. L'[explication officielle SQLite](https://www.sqlite.org/pragma.html#pragma_integrity_check) rappelle qu'`integrity_check` ne détecte pas les erreurs de clés étrangères : le contrôle séparé est indispensable. La réussite sur runner n'est ni une certification de concurrence, ni une restauration opérateur, ni une attestation historique.

## Contrats et limites

- **À qualifier sur nouveau SHA** : 142 tests Rust de base, **6/6** tests dédiés `greenfield_ci_`, **8** gardes source, **118** contrats de continuité. Inventaire textuel revu : 21 appels `database::open_database` uniquement dans `src-tauri/src/greenfield_smoke_tests.rs` sous `#[cfg(test)]` (16 déjà qualifiés + 5 dans la nouvelle fixture). Ces chiffres sont des attentes, pas des PASS.
- Aucun Tauri opérateur, aucun `%LOCALAPPDATA%`, aucun original v6/v7, aucune sauvegarde réelle, ACL, WAL/journal, marqueur réel, migration 007, IPC writer ou release. Aucune exécution Windows ; aucune procédure de restauration réelle autorisée ici.
- Étapes obligatoires : CI `pull_request` au SHA source exact, diff borné/reviews/threads/`Protect main`, squash avec `expected_head_sha`, CI `push` indépendante sur `main`, observation append-only issue #38. Toute commande PowerShell adressée au propriétaire doit être intégralement enveloppée dans `& { ... }`.
- Les 5 scénarios d'archivage déclarés par Laurent restent `OWNER_REPORTED_PASS` seulement, sans témoin indépendant.

**STOP historiques inchangés** : M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; absence d'écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 `OPEN/DRAFT`.
