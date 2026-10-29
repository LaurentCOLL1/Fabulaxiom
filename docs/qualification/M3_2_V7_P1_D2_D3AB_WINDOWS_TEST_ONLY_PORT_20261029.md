# Fabulaxiom M3.2 — portage isolé des preuves D2/D3a/D3b Windows déjà qualifiées (29 octobre 2026)

**Statut : CANDIDAT CI TEST-ONLY. AUCUN RUNTIME / WRITER / RECOVERY / NOUVELLE AUTORISATION D3b-5.**

## Source exacte et raison d'être

La PR [#215](https://github.com/LaurentCOLL1/Fabulaxiom/pull/215) est `OPEN/DRAFT`, `head=8203b7323877edc87ffabaad1694c52d2523023d`, ancienne base `90142d8c78dd8a84ee3f0ee1676a753c8521d78e`, `mergeable=false` face à `main` actuel. Sa CI Windows [#40793962533](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40793962533), source exacte, est SUCCESS (224 Rust, 7 Greenfield, 41 gardes SQLite, 152 contrats). Ne pas forcer sa fusion ni transférer implicitement sa qualification.

La base protégée de cette **nouvelle branche** est `main=820b7cedcdda41bd6fb610e77caa3b4dc122177c`, avec CI postmain indépendante [#40846976948](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40846976948) completed/SUCCESS sur ce SHA. Objectif : incorporer sans conflit de handoff les preuves déjà approuvées, sans inventer D3c/D3d/D3e ou réaliser D3b-4/5.

## Inventaire à empreintes identiques

Les trois fichiers de tests/inventaire ont été copiés **byte pour byte** du HEAD de #215, avec SHA blobs identiques, sous contrôle de diff :

| Chemin relatif | SHA blob source #215 |
|---|---|
| `src-tauri/src/m32_sqlite_vfs_preopen_tests.rs` | `350f5c2e1489af9abe1c11dd7fc18662b4e4f3e6` |
| `tools/m32_rust_sqlite_open_inventory.py` | `724cad9eb0112c0982b829961839a6f9d3686686` |
| `tools/test_m32_rust_sqlite_open_inventory.py` | `083b03306a7a0f729eabeb0a13545be6d67774f2` |

Les six documents historiques originaux sont copiés sans réécriture : design de garde P1, ledger R1–R9, qualifications D2, D3a, D3b, et plan D3. Ces fichiers portent leurs **anciennes preuves SHA/CI** : ils ne revendiquent pas de qualification pour la branche présente.

Le module Rust est déjà importé sur main **uniquement** sous `#[cfg(all(test, windows))]` dans `src-tauri/src/lib.rs`. Base main : 12 tests VFS. Source #215 : 26 tests VFS (12 historiques + 6 D2 + 4 D3a + 4 D3b). Le cas D2 child probe et le cas D3b child fixture sont des helpers `#[test]` déclenchés sous variables d'environnement du processus enfant, sans données opérateur. Les gardes d'inventaire SQL augmentent strictement les comptages attendus à `(22,0,0,0,0,23,0)`, sans nouvelle occurrence dans le runtime.

La CI de cette PR doit prouver **à son propre SHA** : les 26 tests VFS, 14 fonctions D2/D3a/D3b attendues, les gardes de source, les contrats de continuité, sans changer de test Rust de production. Les comptes globaux Windows sont des **attendus** jusqu'à la réussite terminale, jamais des PASS anticipés.

## Frontières inchangées

D3b-4 (témoin durable / replay) et D3b-5 (matrice des phases de crash) **NON IMPLÉMENTÉS**. Aucun nouveau témoin ou nouveau crash-phase stop. Le module D3b existant termine uniquement des processus enfants de tests sur racines %TEMP% fraîches, sous conditions CI Windows, et refuse systématiquement la réouverture SQLite par un successeur. Pas de crash-powerloss, pas d'attestation de récupération. Rien sur `M:\Fabulaxiom` ou `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1`, backups, ACL, WAL/-shm/markers opérateur. Pas de migration 007, S3/S4, IPC, writer production, Windows Hello natif ou Ollama runtime.

STOPs : A0 EXISTING_PROFILE STOP ; R1–R9 production NOT_PROVEN ; writer NOT_PROVEN ; M3.2 IN_PROGRESS_NOT_ACCEPTED ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED ; #35 et #215 OPEN/DRAFT.

**Portage ≠ admission.** Cette nouvelle PR doit rester en **brouillon** tant qu'un audit indépendant du diff et une décision distincte de fusion test-only n'ont pas été enregistrés. Toute nouvelle autorisation D3b-5 doit être explicite et bornée à des fixtures Windows CI jetables. Aucun nouveau code D3b-5 n'est ajouté ici.

## Séquence d'acceptation

Vérifier `Protect main` actif et sans bypass, inventaire test-only, source SHA exact et CI Windows, reviews/threads, absence de modifications runtime, protected merge avec `expected_head_sha` **uniquement après décision sur cette PR**, puis une CI indépendante postmain. Append-only #38 et synchronisation des deux prompts, handoffs, roadmaps. En cas de STOP, garder le brouillon et ne pas remplacer les tests historiques déjà qualifiés.
