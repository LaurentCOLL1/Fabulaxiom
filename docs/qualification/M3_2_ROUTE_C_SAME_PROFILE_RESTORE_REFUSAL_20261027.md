# Voie C — refus de restauration corrompue dans le même profil (fixture CI)

**27 octobre 2026 — candidat, non qualifié à son propre SHA tant que la CI de cette PR n'a pas terminé.**

## Point de départ vérifié

- [PR #186](https://github.com/LaurentCOLL1/Fabulaxiom/pull/186) **MERGED** : source `ad202a0310c378bdbda430f68d9d8686f59a6e18`, [CI source #40402322000](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40402322000) **SUCCESS** ; squash `main=92160c6401fa8b9f2f1667704fb8f51294fdae72`, [CI postmain #40403984550](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40403984550) **SUCCESS** indépendamment. 140 Rust, 4/4 `greenfield_ci_`, 116 contrats. [Checkpoint append-only #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6427938179).
- Profil Windows **déjà fonctionnel** `com.fabulaxiom.greenfield.v1` : **le conserver**. Une destination de test distincte ne commande jamais de créer un deuxième profil opérateur.
- Le service de sauvegarde utilise `VACUUM INTO` pour une copie SQLite cohérente ([documentation SQLite](https://www.sqlite.org/lang_vacuum.html#vacuuminto)), mais une copie interrompue/corrompue doit être **refusée** ; `PRAGMA integrity_check` et `foreign_key_check` ont des contrôles distincts ([SQLite PRAGMA](https://www.sqlite.org/pragma.html#pragma_integrity_check)). Ces propriétés documentées ne constituent aucune preuve Windows opérateur.

## Nouveau cas de refus, strictement jetable

`src-tauri/src/greenfield_smoke_tests.rs` ajoute `greenfield_ci_same_profile_corrupt_restore_refusal_keeps_current_work` :

1. Créer un **unique répertoire temporaire neuf appartenant exclusivement au test** et une SQLite v6 avec un premier Univers ; produire une sauvegarde valide.
2. Ajouter un deuxième Univers **après la sauvegarde**, puis restaurer volontairement la première version **dans le même profil de fixture**. Le fichier original garde le second Univers ; un **autre fichier** devient actif par marqueur. Aucun profil Tauri n'est démarré.
3. Photographier en mémoire les noms de fichiers de `database`, le marqueur actif et ses octets, les octets des deux bases et ceux de la sauvegarde valide.
4. Créer **une deuxième sauvegarde exclusivement pour le test** et corrompre uniquement ce fichier jetable ; demander sa restauration puis une entrée de traversée `../...`. Les deux tentatives doivent échouer.
5. Exiger **aucune nouvelle sélection ni marqueur/fichier de base**, aucun changement aux octets des SQLite et de la sauvegarde valide ; la base sélectionnée reste lisible avec un Univers, l'ancien fichier contient toujours deux Univers.
6. Nettoyer uniquement le répertoire temporaire créé par ce même test. Le poste de Laurent, `%LOCALAPPDATA%`, les originaux v6/v7 et les sauvegardes réelles restent inaccessibles.

## Qualification et plafond de preuve

- Cible à vérifier sur **un nouveau SHA GitHub** : **141 tests Rust** en base, **5/5 scénarios `greenfield_ci_`**, **7 gardes source Greenfield**, **117 contrats de continuité**. L'inventaire textuel des appels `database::open_database` de ce module `#[cfg(test)]` passe de **12 à 16** après revue ; toute ouverture supplémentaire non prévue provoque STOP.
- Les contrôles ne simulent **ni panne électrique pendant l'écriture du marqueur**, ni concurrents réels, ni restauration via la WebView opérateur, ni UI de retour vers l'ancien fichier. Les deux confirmations React restent des gardes source ; aucune attestation indépendante ou autorisation d'essai local ne peut être inférée.
- CI source `pull_request` au SHA exact, diff borné et fichiers de continuité/roadmap revus, absence de review/thread bloquant, `Protect main` actif, fusion `expected_head_sha`, CI postmain `push` indépendante, note append-only issue #38. Les nombres attendus ne valent pas un PASS anticipé.

**STOP maintenus** : M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, absence d'écrivain original `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 `OPEN/DRAFT`. Aucune SQLite originale, sauvegarde privée, ACL, WAL/journal, marqueur opérateur, migration 007, IPC writer, M3.3, ComfyUI ou release touché. Toute future opération Windows exige un consentement **distinct et explicite**, avec commandes PowerShell entièrement encapsulées dans `& { ... }`.
