# M3.2 P2n — deux romans, révisions historiques et corrections par acteur v7 fictif

7 novembre 2026 — **CANDIDAT / NON QUALIFIÉ** avant CI Windows au HEAD exact. Parent protégé `main=2034150b6ccef1bfe015a58ce40a51dd193dd58c` (#310), parent postmain Windows #42406738552 à qualifier indépendamment. Décision `PRODUCT_FIRST_PARALLEL_SAFETY` conservée (prévenir avant tout changement).

## But métier et différence par rapport aux preuves antérieures

Le scénario P1 avait déjà qualifié des opérations v7 sur des fichiers entièrement neufs et jetables ; P2b a déjà un acteur mono-propriétaire sur une connexion v7 RAM préouverte ; P2m a déjà des projections React fictives. P2n ne reconstruit ni ouvreur SQLite, ni UI, ni protocole de transport. Il relie **deux romans du même Univers** à des révisions immuables différentes et aux opérations typées existantes de l'acteur.

Dans `src-tauri/src/m32_p2b_fixture_chronology_actor.rs` uniquement, `#[cfg(test)]` :

1. Deuxième roman u1 avec scène s2, révision historique r4 et HEAD r5 ; troisième roman en u2 avec r6. La base est **RAM inventée préouverte**, aucune ouverture fichier.
2. Ancres u1 sourcées r2 (premier roman) et r4 (second roman), plus une troisième ancre incomparable ; un seul lien chronologique inter-romans explicite. Ancre u2 source r6 séparée. Source u2 injectée dans u1 et relation inter-Univers **refusées** sans perdre les ancres précédentes.
3. Sur les mêmes révisions fictives, prévisualisation d'une correction inter-romans avec `ROLLBACK`, résumé `removed/added`, confirmation explicite par commande indépendante atomique, conservation de l'assertion historique et de la source r4. Aucune autorisation inférée du preview. L'ordre du monde reste partiel ; aucune date, narration ni révélation n'est calculée.

**Deux nouveaux tests Rust attendus** : **330 Rust** (328 + 2), 7 Greenfield, 69 inventaire SQLite, 183 continuité, 396 Vitest, Chromium 85/85 normal+CSP, 19 blobs fictifs. Tous ces nombres sont **ATTENDUS, pas PASS** jusqu'aux journaux Windows du HEAD final.

## Périmètre et STOP

Un seul module Rust `cfg(test)`, une fiche de qualification et fichiers de continuité/roadmap. Ne pas toucher `App.tsx`, `src-tauri/src/lib.rs` runtime, command IPC, ouverture de chemin SQLite, workflow CI, dépendances, scripts de migration 007 ou profils utilisateur. Pas de base opérateur v6/v7, sauvegarde/journal, profil Greenfield existant, Hello natif, marqueur ni recovery. Ce n'est **PAS** une preuve de writer ni une interface opérateur.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimation 40–50 %) ; writer/R1–R9 `NOT_PROVEN`, P4 réel STOP ; G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. Custody atomique main/WAL/SHM et absence d'ABA non observée **NOT_PROVEN**. glib #160 `OPEN_NOT_REMEDIATED`.

Avant fusion : parent postmain #42406738552 SUCCESS au SHA exact ; CI Windows de source au HEAD final terminale SUCCESS ; diff/reviews/threads ; `Protect main` ACTIVE strict bypass=[] ; squash `expected_head_sha` ; postmain indépendant ; issue #38 append-only. Les fixtures CI ≠ admission réelle.
