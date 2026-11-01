# Fabulaxiom — reprise courte (1er novembre 2026)

**01/11 — #256 MERGED** `main=df7171ac99c9f0a6a5e9123de2c8c8168cfb7090`, CI #41308216274/#41309028506 SUCCESS **294/7/67/177**. **CHOIX UTILISATEUR ACTIF : PRODUIT D'ABORD + SÉCURITÉ EN PARALLÈLE** `M3_2_PRODUCT_FIRST_PARALLEL_SAFETY_DECISION_20261101.md` ; P0→P1→P2→P3 sur v7 neuve jetable, R4–R9 en parallèle ; prévenir AVANT tout changement. R4 `M3_2_R4_WINDOWS_TWO_PROCESS_WAL_LOCK_DISPOSABLE_20261101.md`, `M3_2_R4_DELEGATED_MAIN_WAL_NATIVE_HANDLE_FILEID_DISPOSABLE_20261101.md` : fixtures seules ; writer STOP. Protect main strict bypass=[], `expected_head_sha`, #38 append-only.

Reprends Fabulaxiom Windows (React, Tauri v2, Rust, SQLite ; voie C locale, Ollama). Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

**D'abord :** re-fetch GitHub vivant : `main`, PR, issues, CI Windows au SHA exact, reviews/threads et ruleset **Protect main** (strict, zéro bypass). Ce checkpoint ne remplace jamais la vérification du dépôt.

Archives R4 : `M3_2_R4_TWO_CLIENT_POSTOPEN_SHM_IDENTITY_DISPOSABLE_20261101.md`, `M3_2_R4_REGISTERED_OWNER_SHM_SQLITE_NORMAL_WAL_DISPOSABLE_20261101.md`, `M3_2_R4_OWNED_XSHM_ABI_CALLBACK_REFUSAL_DISPOSABLE_20261101.md`, `M3_2_R4_NATIVE_HELD_SHM_LOCKFILEEX_DISPOSABLE_20261101.md`, `M3_2_R4_SHM_HANDLE_BINDING_GATE_RAM_MODEL_20261031.md`, `M3_2_R4_XSHM_REGION0_CALLBACK_VS_HELD_FILE_DISPOSABLE_20261031.md`, `M3_2_R4_XSHM_MAPPED_NT_FILENAME_DECOY_DISPOSABLE_20261031.md`.

R4 qualifiées : `M3_2_R4_NATIVE_HELD_HANDLE_MAP_DISPOSABLE_20261031.md` ; live SQLite WAL-index sur fixtures seulement.

## Dernier checkpoint

- **#242 :** référence `M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md` ; fixtures Win32 uniquement, aucun writer.
- **R3/R4 :** WAL NORMAL refusé sans xShm* ; `M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md`, production NOT_PROVEN. PR #215/#35 DRAFT.

## Interdictions actives — STOP

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`. D3b-4/5 et D3b-5 STOP ; D3c conception seulement.

Ne toucher ni aux données opérateur v6/v7 ni aux journaux/sauvegardes ; aucun IPC writer, migration 007, Windows Hello natif, marqueur persistant ou recovery. Dépôt local : `M:\Fabulaxiom` ; profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` : aucun accès.

## Prochaines opérations

1. PRIORITÉ PRODUIT : P0 matrice acquise ; P1 étendre v7 NEW_ONLY create/list/reopen existant à l'atelier, P2 service fixture, P3 UI isolée.
2. SÉCURITÉ : R2, R4 SHM >0, custody atomique main/WAL/SHM ; R5–R9 STOP ; données opérateur interdites.
3. Conserver le choix entre conversations, alerter avant changement ; deux prompts/handoffs/roadmaps par PR.

Références R4 historiques : `M3_2_R4_D3A_LIVE_SHM_FILEID_DISPOSABLE_20261030.md`.

## Documents d'autorité

Lire d'abord [RESUME_PROMPT.md](RESUME_PROMPT.md), puis `HANDOFF_CURRENT.json`, `HANDOFF_CURRENT.md`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Qualification : [M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md](../qualification/M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md).

**Règle :** fixtures et anciennes CI ne valent jamais admission de données réelles ; archives dans prompt complet et handoffs.
