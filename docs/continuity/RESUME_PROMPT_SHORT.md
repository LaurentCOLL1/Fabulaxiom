# Fabulaxiom — reprise courte (31 octobre 2026)

**#248 FUSIONNÉE :** `main=86133f85162a9efa189d0241ddd27fef8ad2636e` ; source #41214614517 PASS **282/7/60/170**, postmain #41215651418 SUCCESS. **R4 candidat NON QUALIFIÉ :** noms NT `xShmMap` et mapping HANDLE tenu comparés, contrôle leurre aux mêmes octets ; **282/7/61/171 attendus**. Voir `M3_2_R4_XSHM_MAPPED_NT_FILENAME_DECOY_DISPOSABLE_20261031.md`. Référence #248 : `M3_2_R4_XSHM_REGION0_CALLBACK_VS_HELD_FILE_DISPOSABLE_20261031.md`. Pas preuve du HANDLE privé, custody atomique ni writer. CI exact-head, reviews/threads, Protect main strict bypass=[], squash expected_head_sha, postmain et #38 append-only.


**#244 :** CI #41124543182 PASS 269/7/56/166, postmain #41148419366 SUCCESS ; modèle RAM-only `M3_2_R4_SHM_HANDLE_BINDING_GATE_RAM_MODEL_20261031.md` (writer toujours STOP).


Reprends Fabulaxiom Windows (React, Tauri v2, Rust, SQLite ; voie C locale, Ollama). Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

**D'abord :** re-fetch GitHub vivant : `main`, PR, issues, CI Windows au SHA exact, reviews/threads et ruleset **Protect main** (strict, zéro bypass). Ce checkpoint ne remplace jamais la vérification du dépôt.

Références R4 qualifiées : `M3_2_R4_NATIVE_HELD_HANDLE_MAP_DISPOSABLE_20261031.md` ; live SQLite WAL-index sur fixtures seulement.

## Dernier checkpoint

- **#242 :** référence `M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md` ; fixtures Win32 uniquement, aucun writer.
- **R3/R4 :** WAL NORMAL refusé sans xShm* ; `M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md`, production NOT_PROVEN. PR #215/#35 DRAFT.

## Interdictions actives — STOP

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`. D3b-4/5 et D3b-5 STOP ; D3c conception seulement.

Ne toucher ni aux données opérateur v6/v7 ni aux journaux/sauvegardes ; aucun IPC writer, migration 007, Windows Hello natif, marqueur persistant ou recovery. Dépôt local : `M:\Fabulaxiom` ; profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` : aucun accès.

## Prochaines opérations

1. Vérifier la qualification CI exact-head du candidat, diff/reviews/threads, Protect main strict bypass=[], squash `expected_head_sha` si admissible, postmain indépendante et #38 append-only.
2. Continuer **P1, R2/R3, R4 xShm*/WAL/SHM/FileId128**, puis R5/R6/R8 et R7/R9 sur fixtures neuves sans promotion production.
3. Actualiser les deux prompts, handoffs et roadmaps à chaque PR.

Références R4 historiques : `M3_2_R4_D3A_LIVE_SHM_FILEID_DISPOSABLE_20261030.md`.

## Documents d'autorité

Lire d'abord [RESUME_PROMPT.md](RESUME_PROMPT.md), puis `HANDOFF_CURRENT.json`, `HANDOFF_CURRENT.md`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Qualification : [M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md](../qualification/M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md).

**Règle :** fixtures et anciennes CI ne valent jamais admission de données réelles ; archives dans prompt complet et handoffs.
