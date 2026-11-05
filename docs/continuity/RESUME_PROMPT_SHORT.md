# Fabulaxiom — reprise courte (5 novembre 2026)

**#285 P2g FUSIONNÉE** main=`906ad4103a639eaee94f6cb51e55d96cb87f46e0` ; source SHA `6852834fe99a15a1719f45a4997641fd3c76ec86`, Windows #41958673635 SUCCESS **317 Rust/7 Greenfield/68 inventaire/183 continuité, 6 Vitest, Chromium 85/85+CSP, 19 blobs** ; postmain #41967078610 À QUALIFIER au SHA exact. #284 postmain #41958460615 PASS ; #283 postmain #41956730569 PASS. P2g : listes avant/après du graphe actif, IMMEDIATE puis ROLLBACK sur v7 RAM fictive préouverte, sans admission writer/P4. Documentation à actualiser sous PR protégée.

**PRODUCT_FIRST_PARALLEL_SAFETY inchangée**, avertir AVANT changement. glib 0.18.5 Linux GTK3 issue #160 OPEN_NOT_REMEDIATED. **Protect main** active, strict, bypass=[], status Windows obligatoire, squash `expected_head_sha`, nouvelle postmain indépendante, issue #38 append-only (dernier checkpoint #6649577095). Dépôt Windows React/Tauri v2/Rust/SQLite/Ollama : https://github.com/LaurentCOLL1/Fabulaxiom

**D'abord :** re-fetch `main`/PR/issues/CI Windows SHA exact, reviews/threads et ruleset Protect main. Lire `docs/continuity/RESUME_PROMPT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_CURRENT.md`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md`, `docs/roadmap/ROADMAP_STATUS_CURRENT.md`, `FABULAXIOM_ROADMAP_V1.md`.

**Documents récents** : P2g `M3_2_P2G_ACTIVE_GRAPH_PREVIEW_DIFF_FIXTURE_20261105.md`, P2f `M3_2_P2F_DRY_RUN_CHRONOLOGY_CORRECTION_FIXTURE_20261104.md`, P4b `M3_2_P4B_CHROMIUM_FICTIONAL_STAGED_REVIEW_20261103.md`, P3e `M3_2_P3E_HISTORY_INSPECTION_CHROMIUM_PROOF_20261103.md`, P2b `M3_2_P2B_SINGLE_OWNER_CHRONOLOGY_ACTOR_RAM_FIXTURE_20261101.md`, R4 `M3_2_R4_WINDOWS_TWO_PROCESS_WAL_LOCK_DISPOSABLE_20261101.md`. Décision `M3_2_PRODUCT_FIRST_PARALLEL_SAFETY_DECISION_20261101.md`, alerte `M3_2_GLIB_ALERT1_UPSTREAM_BLOCKER_20261101.md`.

## STOP invariants

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; P4 réel STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. R4–R9 vraie custody atomique main/WAL/SHM et exclusion écrivain adversarial NOT_PROVEN. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN` ; D3b-4/5 STOP, D3c conception.

Interdit : données opérateur v6/v7, journaux/sauvegardes, IPC writer, migration runtime 007, Hello natif, marqueur/recovery. Local `M:\Fabulaxiom`, profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` : aucun accès.

## Prochaines opérations

1. Qualifier postmain indépendante #41967078610 ; la source #41958673635 ne remplace jamais la postmain.
2. Continuité documentaire en PR DRAFT, CI Windows propre avant fusion sous Protect main.
3. P1/P2/P3 product-first sur fixtures fictives ; P4 gate séparé ; R2/R4 SHM >0 et custody main/WAL/SHM en parallèle ; R5–R9 STOP ; glib #160 OPEN.

**CI fixtures ≠ admission réelle.**