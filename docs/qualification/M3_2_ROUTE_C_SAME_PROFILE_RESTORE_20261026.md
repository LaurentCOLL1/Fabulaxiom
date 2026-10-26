# Voie C — restaurer dans le profil Greenfield existant, sans le remplacer

**26 octobre 2026 — candidat source/fixtures uniquement : `SAME_PROFILE_RESTORE_RUNNER_ONLY` / `NO_OPERATOR_EXECUTION`.**

Point de départ re-fetch : [PR #185](https://github.com/LaurentCOLL1/Fabulaxiom/pull/185) MERGED, source `84087eb4093b9a72b35b7ea2d6376fcce52c1ddf` / CI #40391038879 `SUCCESS`, `main=03c205f18e4b8c7ed4780ad746d9229e7e910e2c` / postmain #40392826209 `SUCCESS` indépendante, [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6426334227). Le profil opérateur existant `com.fabulaxiom.greenfield.v1` **n'est pas à refaire**. Ses cinq scénarios d'archivage de révisions restent `OWNER_REPORTED_GREENFIELD_REVISION_ARCHIVE_5_OF_5_PASS`, sans attestation indépendante.

## Trois objets à ne pas confondre

| Objet | Statut / rôle |
| --- | --- |
| **Profil Tauri** `com.fabulaxiom.greenfield.v1` | Identité persistante de l'application « PROJETS NEUFS ». Elle ne change pas lors d'une restauration M1.5. |
| **Fichier SQLite actif** | Le profil peut passer de `database/fabulaxiom.sqlite3` à un nouveau `database/fabulaxiom-restored-<token>.sqlite3` par un marqueur `database/activations/activation-<token>.active`. L'ancien fichier n'est pas effacé ; la sélection visible change. |
| **Racine de fixture CI** | Répertoire temporaire créé par un test sur runner Windows jetable. Une racine différente était employée par PR #185 pour l'essai d'import **isolé**, pas parce qu'un second profil serait nécessaire à l'utilisateur. |

Le workflow UI M1.5 existant dans `src/BackupWorkspace.tsx` affiche une confirmation puis exige `RESTAURER`, invoque `restore_database_backup` et recharge la page afin que les lecteurs réouvrent la base nouvellement active. Le backend `src-tauri/src/backup.rs` réserve des fichiers uniques, valide le contenu et n'active que la nouvelle copie après réussite. Le choix de restauration vers une ancienne sauvegarde fait volontairement disparaître *de la vue active* les modifications postérieures à cette sauvegarde ; elles subsistent dans l'ancien fichier, pas dans la version restaurée. C'est un changement fonctionnel à présenter clairement, et non une suppression du profil.

SQLite décrit `VACUUM INTO` comme une copie transactionnellement cohérente qui laisse le fichier source inchangé, tout en avertissant qu'une interruption peut laisser la sortie incomplète. Source primaire : https://www.sqlite.org/lang_vacuum.html#vacuum_with_an_into_clause . Ce mécanisme ne prouve ni l'absence de writer historique ni l'identité d'une source ancienne.

## Nouveau scénario de qualification Greenfield

`greenfield_ci_same_profile_restore_keeps_previous_database_and_archives` dans le module Rust `#[cfg(test)]` :

1. Dans **une seule racine temporaire** de profil neuf, créer univers/roman/chapitre/scène, deux révisions dont l'ancienne est archivée dans `app_metadata` v6 ; fermer la connexion.
2. Créer et conserver une sauvegarde v6 validée ; puis continuer le travail dans **la base active originale** : troisième révision et désarchivage de la première ; fermer.
3. Restaurer la sauvegarde **dans la même racine applicative fictive** : nouveau fichier et marqueur, sans remplacer l'ancienne base ni changer son contenu ou le backup.
4. Simuler le rechargement UI par `resolve_active_database_path` et une nouvelle connexion : vérifier seulement les deux révisions de la sauvegarde, tête `rev-same-2`, texte immuable, archivage de `rev-same-1`, schéma v6.
5. Rouvrir par son chemin explicite l'ancienne SQLite du **runner** : vérifier la troisième révision et le désarchivage postérieurs conservés. Faire une nouvelle sauvegarde dans le **même** profil, avec un nom différent, sans écraser la première.

Les trois scénarios existants de PR #185 (restauration vers une racine séparée, copie corrompue refusée, bascule sur racine occupée) demeurent. Ils ne sont pas des autorisations d'exécution opérateur. L'inventaire textuel Rust passe de 8 à **12** appels de test `database::open_database(`, tous sur fixtures temporaires ; un 13e appel inattendu demeure veto. Six gardes source contrôlent en plus le texte UI, les deux confirmations, le rechargement et les limites de la preuve.

## Conditions avant l'essai sur Windows de Laurent

- **Aucune recréation du profil Greenfield**. Le bon profil reste celui qui fonctionne déjà. On ne touche pas au répertoire `%LOCALAPPDATA%` pendant cette PR de source/fixtures.
- Avant une première sauvegarde réelle : re-fetch du SHA, qualification du build, identification du seul profil neuf, état de l'application/écrivains, chemin de backup dans ce profil, espace disponible, mécanisme d'abandon et accord opérateur ciblé. Le fait que l'interface existe ne prouve pas la sûreté d'un essai particulier.
- Avant une restauration réelle : vérifier que la sauvegarde est bien choisie, expliquer la perte de visibilité du travail postérieur (sans suppression physique), préserver l'ancienne base, valider la copie, contrôler les connexions et le rechargement, puis demander une autorisation distincte. La saisie `RESTAURER` n'est pas à elle seule une attestation de sûreté.
- Ne fournir aucune commande PowerShell sans son texte entier encapsulé dans `& { ... }` et accord nouveau sur ses effets. Aucune procédure automatique ne doit modifier la SQLite opérateur actuelle dans cette tranche.

**STOP inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer historique `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective historique `NOT_STARTED`, PR #35 OPEN/DRAFT. Aucun original SQLite v6/v7, backup historique, ACL, sidecar, journal, marqueur original, migration 007 ou IPC writer touché. La preuve de CI runner et le rapport d'archivage opérateur ne sont pas des attestations interchangeables.
