# M3.2 P2a — Service chronologique typé sur connexion de test préouverte

1er novembre 2026 — CANDIDAT / NON QUALIFIÉ AVANT CI SOURCE EXACT-HEAD. Parent #258 fusionnée : main a51b9660d0d5470ed0d2084a0b733ab8e794ace5 ; CI #41338290444 et #41339303494 SUCCESS, P1 dossier v7 NEW_ONLY fictif qualifié.

## Ce qui est implémenté

Un nouveau module Rust src-tauri/src/m32_p2_fixture_chronology_service.rs, enregistré UNIQUEMENT sous #[cfg(test)] dans lib.rs : API typée pour calendrier, ancre, précédence et snapshot par Univers. Il emprunte une connexion v7 RAM déjà ouverte par un test ; il n'ouvre jamais un chemin SQLite ni n'émet une commande Tauri. Avant opération, il refuse schema !=7, transaction active, lecture seule, foreign_keys OFF, query_only ON, ATTACH inattendu et tables chronologiques absentes.

L'opération create_anchor_with_optional_relation réutilise m32_manual_chronology et englobe une ancre plus sa relation humaine dans une seule transaction BEGIN IMMEDIATE. Une relation invalide provoque un rollback, pas une ancre orpheline. Les relations existantes peuvent être créées séparément ; le snapshot filtre l'Univers, sans produire d'ordre mondial total automatique.

Trois nouveaux tests RAM fictifs, réutilisant la fixture v6 RAM existante sans nouvel appel SQLite open (une unique occurrence ATTACH DATABASE test-only est ajoutée à l'inventaire explicite) : r2 historique reste source, r3 reste révision courante, u1 et u2 séparés ; échec d'un lien provoque rollback complet, cycle et univers étranger refusés ; v6, query_only, clés étrangères OFF et ATTACH sont refusés. P1 reste la preuve complémentaire de persistance v7 NEW_ONLY sur disque : P2a n'ajoute aucun accès fichier.

## Limites

Ce service n'est PAS encore connecté au PreparedV7Writer ; celui-ci est non câblé et la validation de version normale reste v6. L'activer pour le vrai profil, créer un token d'admission, exposer une IPC, monter l'UI App.tsx, enregistrer migration 007 production ou toucher aux données opérateur demeure interdit. Suite P2b : étudier une liaison acteur STRICTEMENT test-only, puis P3 : UI React fictive isolée avec statut transparent. Priorité PRODUCT_FIRST_PARALLEL_SAFETY inchangée ; prévenir le propriétaire AVANT changement de stratégie.

CI source attendue mais NON ACQUISE : 297 Rust / 7 Greenfield / 68 inventaire / 180 continuité. Avant fusion : inspecter diff, reviews/threads, Protect main ACTIVE strict bypass=[], CI Windows SHA exact, squash expected_head_sha et postmain indépendante ; #38/#160 append-only. glib 0.18.5 / Dependabot #1 OPEN_NOT_REMEDIATED, pas de bump direct vers 0.20 ni dismiss.

STOP : M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED. Aucun profil réel %LOCALAPPDATA%\com.fabulaxiom.greenfield.v1, aucune base opérateur v6/v7, backup/sidecar/journal, IPC writer, Hello natif, marqueur, recovery, activation.
