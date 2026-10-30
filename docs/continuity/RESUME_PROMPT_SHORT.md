# Fabulaxiom — reprise courte (30 octobre 2026)

Reprends le développement de l'application Windows **Fabulaxiom** (React, Tauri v2, Rust, SQLite ; voie C locale et Ollama). Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

**D'abord :** re-fetch GitHub vivant : `main`, PR, issues, CI Windows au SHA exact, reviews/threads et ruleset **Protect main** (strict, zéro bypass). Ce checkpoint ne remplace jamais la vérification du dépôt.

## Dernier checkpoint

- PR **#239 fusionnée** : `main=3288bc5099428d2e0f758dfd4ac8eb8707737c8f` ; CI source #41064116889 SUCCESS (263/7/51/161), postmain #41068824429 à vérifier.
- **R3** : matrice Win32 SHARED/RESERVED/PENDING/EXCLUSIVE validée sur fixtures ; nouveau test erreur SHARED/fermeture **NON QUALIFIÉ** (265/7/52/162 attendus). R3 production et R4 WAL/SHM NOT_PROVEN ; PR #215/#35 DRAFT.

## Interdictions actives — STOP

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`. D3b-4/5 et D3b-5 **STOP** ; D3c : conception seulement.

**Ne pas toucher aux données opérateur v6/v7**, ni à leurs journaux ou sauvegardes ; pas d'IPC writer, migration 007, Windows Hello natif, marqueur persistant ou recovery. Dépôt Windows : `M:\Fabulaxiom` ; profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` : **aucun accès**.

## Prochaines opérations

1. Vérifier la CI postmain #239 et l'état actuel de #38 / #215 / #35.
2. Continuer **P1, R2/R3** (verrous SQLite Win32 complets), **R4** (WAL/SHM), puis **R5/R6/R8**, **R7/R9** sur fixtures neuves ; ne pas promouvoir les preuves de test en admission production.
3. Toute PR : diff, reviews/threads, CI Windows **exact-head SUCCESS**, Protect main sans bypass, fusion `expected_head_sha` seulement si admissible, CI postmain indépendante, journal #38 append-only ; actualiser les **deux prompts et roadmaps**.

## Documents d'autorité

Lire en premier [RESUME_PROMPT.md](RESUME_PROMPT.md) (preuves et archives), puis `HANDOFF_CURRENT.json`, `HANDOFF_CURRENT.md`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` ; `docs/roadmap/ROADMAP_STATUS_CURRENT.md` et `docs/roadmap/FABULAXIOM_ROADMAP_V1.md`. Qualification candidate : `docs/qualification/M3_2_R3_READONLY_SHARED_FAILURE_AND_CLOSE_CLEANUP_DISPOSABLE_20261030.md`.

**Règle :** ne jamais extrapoler les fixtures aux données réelles. CI/SHA et inventaires historiques restent dans le prompt complet et les handoffs, pas ici.
