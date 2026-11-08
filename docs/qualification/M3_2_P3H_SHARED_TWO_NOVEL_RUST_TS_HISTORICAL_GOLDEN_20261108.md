# M3.2 P3h — un golden partagé Rust / TypeScript sur deux romans historiques

8 novembre 2026 — **CANDIDAT NON QUALIFIÉ**. Parent protégé `main=4ac62a3f7c0e2cc7a30983a24e843caf753b6c8d` (#316), postmain Windows #42445057666 à qualifier. La stratégie PRODUCT_FIRST_PARALLEL_SAFETY reste active, prévenir AVANT tout changement.

## But produit

Réduire l'écart entre la preuve P2n Rust en SQLite fictive v7 RAM et la revue P3f/P3g TypeScript sans fabriquer un pont SQL/IPC. Le **même fichier Git immuable** `fixtures/m32_p3h_two_novel_historical_contract_v1.json` déclare deux romans distincts du même Univers u1 : roman n1/scène s1/r2 historique/HEAD r3/ancre novel-one-anchor ; roman n2/scène s2/r4 historique/HEAD r5/ancre novel-two-anchor. Seule la précédence directe novel-one-anchor→novel-two-anchor est explicitement déclarée ; independent-anchor reste incomparable ; u2/r6 est étrangère.

## Contrôles indépendants

- `src-tauri/src/m32_p2b_fixture_chronology_actor.rs`, nouveau `#[cfg(test)]` : parse ce JSON via `include_str!`, établit **sur SQLite RAM préouverte seulement** à qui appartiennent r2/r4 et leurs HEAD à l'aide de jointures SQL, exerce les commandes typées de l'acteur et vérifie l'ordre partiel, l'absence de relation sur independent-anchor et le refus de r6 dans u1.
- `src/m32P3hTwoNovelCrossLanguageGolden.test.tsx`, quatre tests Vitest : parse le **même** JSON, vérifie les STOP de provenance, construit une entrée fictive P3f avec quatre témoins déclaratifs et une correction inventée, valide les assertions directes sans ordre total, refuse propriétaires/révisions étrangers et cycles avant affichage.
- Aucun nouveau `App.tsx`, IPC, import navigateur runtime, ouverture de fichier, base opérateur, workflow, dépendance ou lockfile. Le Rust et le TS **ne communiquent pas** : ce sont deux tests indépendants du même blob Git. Les relations de UI restent entièrement fictives ; le test Rust ne valide pas un contrat de transport réel.

## CI et admissions

**Avant CI : attendus NON PASS** 331 Rust (330+1), 7 Greenfield, 69 inventaire SQLite, 183 continuité, 408 Vitest (404+4), 88/88 Chromium normal+CSP stricte, 25 blobs Git fictifs du manifeste navigateur fermé préexistant. Parent postmain au SHA exact, CI source HEAD final, diff/reviews/threads, Protect main ACTIVE strict bypass=[], guarded squash `expected_head_sha`, postmain indépendant, #38 append-only.

M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimation), writer/R1–R9 `NOT_PROVEN`, P4 réel STOP, G2B `NOT_ACCEPTED`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, custody atomique main/WAL/SHM et ABA non observée `NOT_PROVEN`, glib #160 `OPEN_NOT_REMEDIATED`. Aucune donnée opérateur v6/v7, profil Greenfield existant, backups/journaux, IPC writer, migration 007 runtime, Windows Hello natif, marqueur ou recovery. Fixtures CI ≠ admission réelle.
