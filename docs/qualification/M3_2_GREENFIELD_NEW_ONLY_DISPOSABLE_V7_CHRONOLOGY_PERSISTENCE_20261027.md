# M3.2 — premier témoin de persistance réelle, projet neuf v7, fichiers CI jetables

Date : 27 octobre 2026. **CANDIDATE SOURCE/TEST UNIQUEMENT ; ne constitue ni l'acceptation de M3.2 ni une autorisation d'exécution sur le poste Windows.** Référence de départ vivante : PR #190 fusionnée, squash `main=7c7e02899784e52e3eb06dfff9d79a613eec95c1`, postmain indépendante #40462274918 `SUCCESS`. Le test introduit dans cette candidate exige **sa propre CI au SHA exact**.

## Périmètre minimal réellement couvert

- `src-tauri/src/world_time_file_migration_tests.rs` : test Rust `#[cfg(test)]` `m32_new_only_disposable_v7_chronology_survives_reopen_without_touching_prior_v6` ; deux SQLite de fiction **créées par le test dans un dossier temporaire de runner**. Une ancienne fixture v6 est fermée et gelée ; une **autre** fixture v6 est créée séparément, puis équipée du candidat de schéma M3.1 v7 et des décisions immuables M3.2 dans une transaction exclusivement sur cette seconde base. **Aucune copie/migration de l'ancienne fixture vers la nouvelle.** La ligne v7 du registre est simulée dans la nouvelle base jetable seulement, sans enregistrer 007 dans les migrations de production.
- Écriture de calendrier fictif, ancre exacte liée à une révision source immuable, ancre inconnue, ordre explicite, tentative de cycle rejetée, tentative inter-univers rejetée, supersession atomique conservant l'ancienne ancre. Vérification de l'intégrité SQLite et des FK.
- Fermeture réelle de la connexion SQLite, **réouverture explicite en lecture/écriture de la même base jetable**, relecture de l'ordre, de la décision, des ancres courantes, du texte et des données M2 préexistantes ; comparaison octet pour octet de la fixture v6 distincte et absence de changement de marqueur.
- `tools/m32_rust_sqlite_open_inventory.py` : compte rendu textuel exact de **deux** nouvelles ouvertures SQLite `READ_WRITE` `#[cfg(test)]`. Ce contrôle de sources ne prouve pas à lui seul la sûreté d'un runtime.

## Ce que cela ne prouve pas

Ni parcours utilisateur Tauri/React, ni stockage M3.2 dans le **profil Windows déjà fonctionnel** `com.fabulaxiom.greenfield.v1`, ni sauvegarde/restauration d'une vraie base opérateur, ni qualification d'un ouvreur v7 de production, ni IPC écrivain, ni migration 007 automatique. Aucune SQLite originale v6/v7, ACL, backup, WAL/journal, activation, marqueur ou historique privé n'est manipulé. La réussite éventuelle en CI est attachée **au SHA précis de cette candidate** et n'est pas une attestation indépendante Windows.

## Séquence de levée de blocage sans changer de profil

1. **Maintenant :** obtenir la CI Windows exacte du témoin de persistance sur disque de runner ; vérifier diff, reviewers, threads et `Protect main`, puis fusion protégée et postmain indépendante.
2. **Ensuite (nouvelle PR, nouveau gate) :** proposer un ouvreur/contrat de propriété v7 **réservé aux nouveaux projets**, incapable d'ouvrir ou de convertir une base préexistante non explicitement qualifiée ; intégrer de vrais appels métier M3.2 puis les scénarios de fermeture/relance UI, en CI jetable d'abord.
3. **Avant toute opération opérateur :** revue d'un protocole d'exécution dans le profil existant sans écrasement, refus robuste si état ambigu, sauvegardes et restauration testées, preuves indépendantes et consentement spécifique aux opérations sensibles encore exclues. Ne pas inventer les cinq attestations de la voie historique.

STOP inchangés : M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer historique `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 `OPEN/DRAFT` non fusionnable. Le profil `com.fabulaxiom.greenfield.v1` reste l'unique profil opérateur ; aucun autre n'est demandé. Toute commande PowerShell destinée au propriétaire doit être entièrement encapsulée dans `& { ... }`.
