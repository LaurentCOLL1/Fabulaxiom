# Voie C — qualification de sauvegarde/restauration des projets neufs (26 octobre 2026)

**Addendum daté après PR #185 :** à la demande de Laurent, il est confirmé qu'**aucun nouveau profil Tauri** n'est nécessaire. L'interdiction `EXISTING_PROFILE_RESTORE_BLOCKED` ci-dessous était une décision conservatoire **d'exécution opérateur non qualifiée au checkpoint PR185**, pas un veto à la fonction M1.5 ni une preuve qu'elle écrase un fichier. L'API existante crée déjà un nouveau fichier sous le même profil, préserve physiquement l'ancien et change volontairement l'activation après confirmation. Nouvelle qualification sur ce vrai parcours, **fixtures seulement** : [M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md](M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md). Aucun geste Windows ne découle de cet addendum.

**Statut : `RUNNER_ONLY` / `EXISTING_PROFILE_RESTORE_BLOCKED` / `NO_OPERATOR_EXECUTION`.**
Cette tranche source/fixtures ne constitue ni une procédure Windows, ni une sauvegarde réelle du poste, ni une qualification de distribution. Base de départ vérifiée avant travail : PR #184 MERGED, `main=810a31b22dabb0507d43d83dd1b5b374916bf13b`, CI postmain #40338104050 `SUCCESS`. Ces SHA sont des preuves datées, pas le futur HEAD de la présente PR.

## Justification et risques

- Le profil DEV `com.fabulaxiom.greenfield.v1` a été exercé sur Windows avec archivage de révisions `OWNER_REPORTED_GREENFIELD_REVISION_ARCHIVE_5_OF_5_PASS`, sans preuve indépendante. Le stockage de préférence utilise `app_metadata` v6 et ne détruit jamais le texte d'une révision.
- `backup::create_backup` valide la source puis appelle `database::open_database` et `VACUUM INTO` sur une destination réservée unique. Dans les tests, **la source est uniquement une SQLite v6 créée par le runner**. Il ne faut pas transférer le raisonnement à une SQLite historique ou au profil opérateur sans revoir les entrées et effets.
- `backup::restore_backup` valide le fichier, copie dans un **nouveau fichier** puis publie un marqueur d'`activation` append-only. Il ne remplace pas les octets de l'ancienne base, **mais accepte actuellement un répertoire applicatif déjà occupé et change alors la base active**. C'est un risque fonctionnel réel pour une session Greenfield existante : `EXISTING_PROFILE_RESTORE_BLOCKED` au niveau de la décision de procédure, **pas un blocage déjà implémenté dans l'API**.
- Un `VACUUM INTO` terminé crée une image transactionnellement cohérente selon la documentation SQLite ; une interruption peut produire un fichier incomplet, ce qui motive la validation et l'absence d'activation après échec. Cela ne prouve ni provenance historique ni absence d'écrivain original. Référence : https://www.sqlite.org/lang_vacuum.html#vacuum_with_an_into_clause .

## Matrice de qualification sur runner Windows jetable

| Contrôle | Attendu / plafond de preuve |
| --- | --- |
| `greenfield_ci_m1_m2_lifecycle_and_separate_destination_restore` | Source v6 neuve ; univers/série/roman/chapitre/scène, deux textes immuables, fait sourcé et revue humaine fictive. Archivage de l'ancienne révision dans `app_metadata`, fermeture, backup, copie vers une autre racine neuve, restore ; texte courant et ancien, préférence d'archivage, compteurs, provenance, schéma v6 inchangés ; source et backups identiques en octets après restauration. |
| `greenfield_ci_corrupt_backup_cannot_activate_a_fresh_restore_root` | Copie volontairement corrompue dans une racine temporaire neuve : refus et aucun fichier actif ni marqueur publié ; source et backup originaux inchangés. |
| `greenfield_ci_occupied_restore_root_switches_selection_so_operator_use_is_blocked` | Contre-exemple **négatif** dans deux racines temporaires : l'API M1.5 conserve le fichier existant mais change la sélection active. Ce test ne valide PAS cette opération sur le poste ; il documente la garde absente. |
| `tools/test_m32_greenfield_backup_restore.py` | Cinq gardes source empêchant de confondre tests `#[cfg(test)]`, CI runner et autorisation utilisateur. |

Les fixtures créent exclusivement des répertoires uniques dans `temp_dir()` avec création exclusive `create_dir` et ne les suppriment qu'après fermeture des connexions. La CI filtre les tests `greenfield_ci_` dans `src-tauri/src/greenfield_smoke_tests.rs` ; aucune commande Tauri/UI ni accès réseau du test n'est impliqué.
L'inventaire textuel `tools/m32_rust_sqlite_open_inventory.py` recense désormais **8** appels `database::open_database(` dans ce module `#[cfg(test)]` contre 3 auparavant. Les cinq nouveaux appels sont relus comme exclusivement créés par ces fixtures ; l'inventaire garde son STOP fail-closed sur un neuvième appel imprévu. Ce comptage n'est pas une preuve d'identité Windows.

## Conditions minimales avant un geste opérateur distinct

1. Une API/procédure dédiée doit **refuser avant toute copie ou activation** une cible existante, réparse/symlink, ambiguë ou ouverte, puis réserver atomiquement une **nouvelle** racine distincte ; décider comment authentifier identité et provenance du backup neuf.
2. Prévoir fermeture contrôlée de l'application, contrôles de taille/espace/ACL et journaux sous Windows, erreurs partielles, restauration vérifiée sans modifier l'original, mécanisme d'abandon et présentation claire de la nouvelle destination. Ne pas simplement appeler `restore_database_backup` sur le profil vivant.
3. Tester cas adversariaux et requalifier la CI du **HEAD exact**, puis demander à Laurent le **code PowerShell intégral sous `& { ... }`**, effets, entrées, STOP et un consentement explicite nouveau si une exécution Windows devenait pertinente.
4. Une PR distincte sera nécessaire avant activation utilisateur, écriture ou remplacement de `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3` ; aucune restauration automatique ni release.

## Frontières inchangées

Voie C `DEVELOPMENT_ONLY`. M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain historique `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective historique `NOT_STARTED`, PR #35 `OPEN/DRAFT`. Aucun SQLite original v6/v7, sauvegarde historique, ACL, WAL/journal, marqueur original, migration 007 ou IPC writer touché. Les anciennes CI et les rapports `OWNER_REPORTED` n'attestent pas cette nouvelle tranche.
