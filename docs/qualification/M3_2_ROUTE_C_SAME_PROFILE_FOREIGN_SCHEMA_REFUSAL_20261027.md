# Voie C — refus des sauvegardes d'une autre application ou à migrations falsifiées (CI)

**27 octobre 2026 — candidat SOURCE/FIXTURES UNIQUEMENT, non qualifié sur son futur SHA avant CI.**

## Base d'autorité vivante

- [PR #188](https://github.com/LaurentCOLL1/Fabulaxiom/pull/188) **MERGED**, source exacte `9ca23c1b78c5fb2e3f49c2c3728024be374caeba` / [CI #40450684268](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40450684268) `SUCCESS`, fusion squash protégée `main=e4cd6ba8151f2d6cbab8723d2fb200d3ac3ffebc` / [postmain indépendante #40451602743](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40451602743) `SUCCESS`. 142 tests Rust, 6/6 fixtures Greenfield, 8 gardes source, 118 contrats ; [issue #38 append-only](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6434133177).
- Le profil Windows de Laurent **`com.fabulaxiom.greenfield.v1` existe déjà, fonctionne selon le propriétaire et DOIT être conservé**. Dans la voie C, une restauration valide crée **un autre fichier SQLite à l'intérieur du même profil**, sans écraser l'ancienne base ; aucune deuxième destination Tauri n'est requise.

## Test supplémentaire de provenance de sauvegarde

Dans `src-tauri/src/greenfield_smoke_tests.rs`, le test `greenfield_ci_same_profile_foreign_owner_and_lineage_backup_refusals` doit :

1. Créer une SQLite v6 neuve et exclusivement temporaire sur runner, y inscrire un Univers, générer un backup sain et ajouter un second Univers **après** ce backup dans la base originale.
2. Restaurer le backup sain vers un **autre fichier de la même racine de fixture** ; figer en mémoire les octets des deux SQLite, le marqueur, les noms de fichiers et la sauvegarde saine.
3. Fabriquer une nouvelle sauvegarde jetable et modifier uniquement sa métadonnée `app_metadata.schema_owner` vers `other_application`. Le fichier reste physiquement sain (`PRAGMA integrity_check = ok`) mais n'appartient plus à Fabulaxiom. La restauration doit retourner `integrity` sans changer la base active.
4. Fabriquer une autre sauvegarde jetable, conserver `schema_owner = fabulaxiom` mais changer le **nom** de migration 006 dans `schema_migrations` vers `006_forged_review_log` ; même refus `integrity` sur la lignée incohérente sans activation.
5. Vérifier le marqueur inchangé, aucun nouveau fichier de base sélectionné/créé, les octets d'origine, d'active et des trois sauvegardes inchangés ; le second Univers n'existe que dans l'ancienne base.
6. Nettoyer seulement les fichiers de la racine temporaire créée par cette fixture. Aucun Tauri n'est lancé.

Ces contrôles exploitent les barrières **déjà présentes** dans `backup::read_validated_database`/`validate_connection`. Ils ne prouvent pas l'authenticité cryptographique d'un backup, la résistance à un attaquant maîtrisant tous les fichiers, les garanties de concurrence ou une récupération réelle sur l'ordinateur de Laurent. 

## Qualification et limites

- **Attentes, non encore PASS sur nouveau SHA** : 143 Rust de base, **7/7 `greenfield_ci_`**, 9 gardes source, 119 contrats de continuité ; audit textuel de 27 appels `database::open_database` (21 anciens + 6 nouveaux) exclusivement dans le module `#[cfg(test)]`, chemins de fixture.
- Aucune modification de la logique applicative de sauvegarde, de la migration 007, du writer IPC, de l'archive de texte, de la WebView Tauri ou de la release. Aucune ouverture SQLite originale, sauvegarde opérateur, ACL, WAL/journal, marqueur Windows ou accès `%LOCALAPPDATA%` ; **NO_OPERATOR_EXECUTION**.
- CI exacte `pull_request` sur SHA candidat, diff/reviews/threads, `Protect main`, fusion squash avec `expected_head_sha`, CI `push` postmain indépendante et issue #38 append-only. Les preuves des PR #187/#188 sont historiques et non transposables.
- Archivage 5/5 Windows : `OWNER_REPORTED_PASS`, pas d'attestation indépendante. Toute action future sur Windows local reste distincte d'un simple `Continue` GitHub ; tout PowerShell communiqué à l'opérateur doit être entièrement enveloppé dans `& { ... }`.

**STOP historiques inchangés** : M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 réel `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT.
