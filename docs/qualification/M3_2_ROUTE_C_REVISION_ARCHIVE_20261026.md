# Voie C — archivage réversible des révisions de scène (26 octobre 2026)

**Observation post-implémentation du 26 octobre 2026 :** [PR #183](https://github.com/LaurentCOLL1/Fabulaxiom/pull/183) source `7879f2b052944d68ca367537809b0af8e05bca04`, CI #40309445029 SUCCESS, `main=39725a020a8656b8d0488628bc208fcf104c058c`, CI postmain #40310982760 SUCCESS. L'opérateur Windows confirme explicitement les **cinq points** (archiver/masquer une ancienne, afficher l'archive avec texte intact, désarchiver, persistance après fermeture/réouverture, révision courante toujours visible/non archivable) : `OWNER_REPORTED_GREENFIELD_REVISION_ARCHIVE_5_OF_5_PASS`, **pas d'attestation indépendante**, [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6417653782). Chemins de développement et de base Greenfield [documentés avec limites](../continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md). Cette observation ne change aucune interdiction historique ni M3.2/G3.

**Portée : uniquement le profil Tauri de développement `com.fabulaxiom.greenfield.v1`, projets neufs.** Aucun original M1.5 v6 / M3.1 v7, backup historique, marqueur, ACL, journal, writer IPC, migration 007 ou gate M3.2/G3 n'est qualifié ni sollicité par cette évolution.

## Besoin opérateur

Le 26 octobre 2026, après un premier lancement Windows Greenfield et un parcours de persistance déclarés `OWNER_REPORTED_PASS`, l'opérateur a demandé à pouvoir supprimer des révisions de scène. La source M1.4 conserve délibérément des `scene_text_revisions` immuables : les triggers SQLite `scene_text_revisions_immutable` et `scene_text_revisions_no_delete` bloquent `UPDATE` et `DELETE`, et les faits M2 peuvent citer une révision et un intervalle UTF-8 précis. L'utilisateur a ensuite **choisi explicitement l'archivage/masquage réversible** plutôt qu'une suppression définitive.

## Conception non destructive

- Les révisions demeurent intégralement en SQLite ; aucun `DELETE`/`UPDATE` sur `scene_text_revisions`, sur ses têtes, ses enfants, les faits ou les citations.
- **Aucune migration** : la table `app_metadata` préexistante du schéma v6 contient exclusivement une préférence par identifiant immuable de révision, clé `greenfield_revision_archive:<revision_id>`, valeur `1`. Désarchiver supprime uniquement **cette préférence** de `app_metadata` ; cela ne supprime aucune révision. La sauvegarde normale de cette *nouvelle SQLite* inclut ces préférences ; une sauvegarde préexistante ne nécessite pas de conversion.
- Les commandes `scene_archived_revision_ids` et `set_scene_revision_archived` exigent **avant d'ouvrir une connexion SQLite** que `app.config().identifier` corresponde exactement au profil Greenfield ; autrement `greenfield_only`. `greenfield_revision_archive_enabled` ne consulte que l'identifiant en mémoire et n'ouvre aucune base. Le profil normal ne présente pas les contrôles d'archivage.
- Validation transactionnelle : scène réelle, révision réelle dans cette scène, refus d'archivage de la révision courante, retour idempotent et masquage limité au panneau d'historique. La restauration d'une révision archivée demande d'abord de la désarchiver ; il reste toujours possible de consulter toute la provenance dans SQLite.
- Le filtre d'interface est **un filtre d'affichage**, jamais un filtre de requête Rust sur les révisions. Bouton « Afficher les archivées » puis « Désarchiver » ; le pointeur courant demeure visible, même face à une préférence archivée incohérente.

## Bornes de preuve

Tests Rust sur SQLite **en mémoire fictive** : invariance des textes/parentés/pointeur, refus des révisions courantes ou appartenant à une autre scène, réversibilité/idempotence, schéma toujours v6 et trigger `DELETE` conservé. Tests Vitest : filtre de visibilité, affichage des archives, maintien de la révision courante. CI Windows sur SHA exact et postmain séparée requises avant toute qualification source ; aucune exécution de ces nouveaux contrôles sur le Windows opérateur dans cette PR.

Cette fonction n'est **pas** un effacement de données, un masquage cryptographique, une suppression de contenu sensible, une attestation historique, un traitement de migration v7 ou une release. Si un utilisateur veut une purge irréversible plus tard, il faut une conception distincte des références, des sauvegardes et des contraintes d'audit, avec autorisation explicite.

**STOP inchangés** : M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain original `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 réel `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective historique `NOT_STARTED` ; #35 OPEN/DRAFT.
