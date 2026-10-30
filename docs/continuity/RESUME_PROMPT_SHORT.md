# Fabulaxiom — reprise courte (30 octobre 2026)

Reprends le développement de l'application Windows **Fabulaxiom** (React, Tauri v2, Rust, SQLite ; voie C locale et Ollama). Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

**D'abord :** re-fetch GitHub vivant : `main`, PR, issues, CI Windows au SHA exact, reviews/threads et ruleset **Protect main** (strict, zéro bypass). Ce checkpoint ne remplace jamais la vérification du dépôt.

## Dernier checkpoint

- PR **#241 fusionnée** : `main=03a2b6206e49f0e7aac5b4acbdfcee2d98737b97` ; CI source #41075099123 SUCCESS (266/7/53/163) ; postmain indépendante #41082491631 IN_PROGRESS au checkpoint, à re-vérifier.
- **R3** : deux lecteurs SHARED simultanés qualifiés sur fixtures Windows ; R3 production NON PROUVÉ.
- Nouvelle **candidature R4** : référence WAL/SHM avec VFS Win32 SQLite standard, qualification `M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md` ; **267/7/54/164 attendus NON QUALIFIÉS** jusqu'à CI exact-head. Cela ne prouve PAS les `xShm*` propres au VFS Fabulaxiom ni R4 production. PR #215/#35 DRAFT.

## Interdictions actives — STOP

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`. D3b-4/5 et D3b-5 **STOP** ; D3c : conception seulement.

**Ne pas toucher aux données opérateur v6/v7**, ni à leurs journaux ou sauvegardes ; pas d'IPC writer, migration 007, Windows Hello natif, marqueur persistant ou recovery. Dépôt Windows : `M:\Fabulaxiom` ; profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` : **aucun accès**.

## Prochaines opérations

1. Vérifier la CI postmain #241 ; qualifier la candidature R4 par CI Windows exact-head, diff, reviews/threads, `Protect main` strict, puis fusion `expected_head_sha` uniquement si admissible, CI postmain indépendante et #38 append-only.
2. Continuer **P1, R2/R3**, notamment **R4 `xShm*` WAL/SHM et garde FileId128** sur fixtures neuves, puis R5/R6/R8 et R7/R9. Ne pas promouvoir les fixtures en admission production.
3. Actualiser les deux prompts, handoffs et roadmaps à chaque PR importante.

## Documents d'autorité

Lire d'abord [RESUME_PROMPT.md](RESUME_PROMPT.md), puis `HANDOFF_CURRENT.json`, `HANDOFF_CURRENT.md`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et les deux roadmaps. Qualification candidate : [M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md](../qualification/M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md).

**Règle :** ne jamais extrapoler les fixtures aux données réelles. CI/SHA et inventaires historiques restent dans le prompt complet et les handoffs, pas ici.
