# M3.2 P3a — atelier React de commandes fictives typées

**1er novembre 2026 — CANDIDAT NON QUALIFIÉ tant que la CI Windows de la PR au HEAD exact ne s'est pas terminée.** Parent PR #260 P2b fusionnée sous Protect main, `main=0f2b56dbc07ac2c7db431ab99b93cc653b489341`, CI source #41345394783 SUCCESS 301/7/68/181, postmain indépendante #41347171014 completed/SUCCESS au SHA exact (301/7/68/181).

## Objet réel

Accélérer l'usage futur de Fabulaxiom, conformément à `PRODUCT_FIRST_PARALLEL_SAFETY`, sans traverser le gate du writer réel.

- `src/m32P3FictionalCommandContract.ts` : reducer TS pur et typé, **seulement données fictives en mémoire** ; commandes `create_anchor_with_optional_relation` et `create_precedence`, lecture d'un snapshot borné à l'univers attendu. Contrat inspiré du vocabulaire de l'acteur Rust P2b, **pas d'appel de l'acteur Rust** ni de protocole IPC de production.
- `src/M32P3FictionalCommandWorkshop.tsx` : nouveau formulaire React isolé, dates exactes/approximatives/relatives/inconnues dans le monde fictif ; choix explicite d'une révision narrative historique, possibilité de relation `avant/après` justifiée, retour d'échec et vue d'état locale. Message visible de **non-persistance** et absence de raccord Rust.
- `src/m32BrowserLab.tsx` : lien vers cet écran **uniquement dans le laboratoire fictif** ; aucune modification du runtime `src/App.tsx`.
- `src/m32P3FictionalCommandContract.test.tsx` : 11 cas de contrats et SSR : rollback immuable d'ancre + relation, cycles et doublons refusés, refus univers étranger et source forgée, référence historique `r2` conservée distincte de `r3`, absence d'ordre de révélation inféré, refus d'origine/cycle, rendu React accessible et chaîne HTML inerte.

Cette tranche **n'est pas une intégration de Rust à React**, ni une persistance v7. Le vrai service mono-propriétaire `m32_v7_writer_service.rs` reste non branché. Aucun accès au vrai profil `%LOCALAPPDATA%\\com.fabulaxiom.greenfield.v1`, aux données de `M:\\Fabulaxiom`, ni au SQLite opérateur v6/v7. P3b, après qualification, doit clarifier le contrat entre les deux piles exclusivement dans une fixture CI, **sans IPC de production**.

## Critères de qualification

Tests Vitest projet + 11 tests P3a, CI Windows Chromium/CSP, inventaire SQLite inchangé (68), Rust/Greenfield 301/7, contrat de continuité 182 (valeurs ATTENDUES NON ACQUISES), source SHA exact, diff, reviews/threads, Protect main ACTIVE strict sans bypass, squash `expected_head_sha`, CI postmain indépendante. Aucun changement de stratégie sans prévenir le propriétaire en amont.

## Gates et sécurité inchangés

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED.** Aucune migration 007 runtime, IPC writer, Windows Hello, marqueur/recovery, backup/journaux, identité de source ou custody atomique faussement acquis. GLIB 0.18.5 / GHSA-wrw7-89jp-8q8g Linux GTK3 alerte #1 reste OPEN_NOT_REMEDIATED (#160), pas de changement Cargo.lock ni de dismissal. #38/#160 append-only.
