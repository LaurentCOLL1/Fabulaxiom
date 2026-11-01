# M3.2 P1 — Parcours chronologique de deux romans avec révision historique sur fixture v7 neuve

**1er novembre 2026. CANDIDAT SOURCE / CI WINDOWS NON QUALIFIÉ AVANT RUN EXACT-HEAD.** Décision active de l'utilisateur [produit d'abord + sécurité en parallèle](../continuity/M3_2_PRODUCT_FIRST_PARALLEL_SAFETY_DECISION_20261101.md) ; dernier parent vérifié `main=6346ebd405345e1cc2447cd28fa679bef7f19490` (#257 fusionnée). CI postmain #41331242603 terminée SUCCESS au même SHA, **294 Rust / 7 Greenfield / 67 inventaire / 178 continuité**.

## Petit incrément PRODUIT : réemployer la preuve de persistance existante

**Ne pas reconstruire un ouvreur SQLite** : le test Rust `m32_new_only_disposable_v7_chronology_survives_reopen_without_touching_prior_v6` de `src-tauri/src/world_time_file_migration_tests.rs` crée DÉJÀ deux bases v6 de fiction, réutilise une nouvelle base de test exclusivement dans un `%TEMP%` CI, applique v7 seulement à cette base, fait des CRUD chronologiques, ferme et réouvre le même fichier puis prouve que l'autre base v6 est inchangée.

P1 étend **ce même test**, sans nouvelles ouvertures SQLite : deuxième roman dans le même Univers `u1`, scène et révisions immuables `r2` historique et `r3` tête courante ; deuxième Univers `u2`. Sur `u1`, créer explicitement une ancre **approximative** et une ancre **relative**, toutes deux sourcées par `r2`, plus la relation humaine `approx avant relative`. Exiger le refus d'un cycle inverse et d'un lien d'ancre `u2` vers `r2` appartenant à `u1`. Après fermeture réelle et réouverture **du nouveau fichier inventé**, lister et vérifier les quatre ancres courantes, les deux précédences humaines indépendantes, la source historique `r2` tandis que `r3` reste tête, les deux Univers séparés, les 14 tables v6 intactes et `PRAGMA integrity_check/foreign_key_check`. Aucun ordre total automatique entre événements indépendants.

C'est un scénario **métier sur de vraies écritures disque de fixture** et une étape concrète vers la future UI, **pas encore une interface opérateur, ni une nouvelle implémentation runtime**. L'atelier fictif React existe mais est toujours non monté ; l'adaptateur typé service/React est une tranche P2/P3 distincte. Pas d'Ollama, cloud, profil Tauri, donnée privée, nouveau projet permanent ni exécution sur le PC propriétaire.

## Sécurité parallèle et suivi glib

La capture du propriétaire confirme [Dependabot #1](https://github.com/LaurentCOLL1/Fabulaxiom/security/dependabot/1) GHSA-wrw7-89jp-8q8g toujours OPEN. `glib=0.18.5` n'est pas éligible à un bump isolé vers 0.20 à cause de `gtk=0.18.2` et `webkit2gtk=2.0.2`. Le graphe Windows sélectionné n'inclut pas glib/GTK, mais le graphe Linux le contient ; risque Linux **OPEN_NOT_REMEDIATED**, sans preuve de reachability. Voir [audit séparé](M3_2_GLIB_ALERT1_UPSTREAM_BLOCKER_20261101.md) et [issue #160](https://github.com/LaurentCOLL1/Fabulaxiom/issues/160). La PR P1 ne touche **ni `Cargo.toml` ni `Cargo.lock`**, ne supprime aucun audit, ne dismiss aucune alerte et ne prétend pas réparer une vulnérabilité. Les preuves R4–R9 et les gates de provenance continuent en parallèle.

## Qualification et garde-fous

Cible **294 Rust / 7 Greenfield / 67 inventaire SQLite / 179 continuité ATTENDUS**, et non acquis avant CI source au SHA exact et logs. Diff limité au test déjà `#[cfg(test)]`, documents et contrat source-only ; aucun `App.tsx`, Tauri State/IPC, ouvreur runtime, migration 007 de production, marqueur durable ou recovery. Avant la fusion : `Protect main` strict bypass=[], revues/threads, squash `expected_head_sha`, puis CI postmain indépendante + #38 append-only.

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED.**
