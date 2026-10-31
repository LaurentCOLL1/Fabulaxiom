# Fabulaxiom — reprise courte (31 octobre 2026)

**#245 FUSIONNÉE :** `main=8f582c2f9cf1a7e0a346d3ef9b5258acc1d1d772`; CI source #41149090126 PASS **279/7/57/167** ; postmain #41151561992 SUCCESS au SHA exact. **#246 DRAFT, NON QUALIFIÉE :** test R4 mapping natif sur le même HANDLE d'un -shm fictif `%TEMP%` ; FileId128, **281/7/58/168 ATTENDUS, PAS PASS**. Voir `M3_2_R4_NATIVE_HELD_HANDLE_MAP_DISPOSABLE_20261031.md`. Aucune preuve de véritable SQLite xShmMap, custody atomique ou writer production. STOP inchangé : CI exact-head, diff/reviews/threads, Protect main strict bypass=[], squash `expected_head_sha` seulement si admissible, CI postmain distincte, #38 append-only.


**#244 FUSIONNÉE** sous Protect main : `main=1d06478a161cec35329b4f1ea9a67744fdea0a42` ; source #41124543182 SUCCESS **269/7/56/166**, postmain indépendante #41148419366 à vérifier. **R4 prochain candidat (non qualifié)** : modèle **RAM-only** des exigences de liaison native entre handles main/WAL/SHM et le véritable handle xShmMap ; 10 nouveaux tests, **279/7/57/167 attendus, PAS PASS**. Voir `M3_2_R4_SHM_HANDLE_BINDING_GATE_RAM_MODEL_20261031.md`. Aucun accès SQLite, aucun writer de production.


Reprends Fabulaxiom Windows (React, Tauri v2, Rust, SQLite ; voie C locale, Ollama). Dépôt : https://github.com/LaurentCOLL1/Fabulaxiom

**D'abord :** re-fetch GitHub vivant : `main`, PR, issues, CI Windows au SHA exact, reviews/threads et ruleset **Protect main** (strict, zéro bypass). Ce checkpoint ne remplace jamais la vérification du dépôt.

## Dernier checkpoint

- PR **#242 fusionnée** sous Protect main : `main=6166a256e479ef7cd3c1a6cacdaccaadb68cfb49` ; source #41084067311 SUCCESS (267/7/54/164), CI postmain #41110676555 SUCCESS au SHA exact. Référence R4 précédente : `M3_2_R4_DEFAULT_WIN32_WAL_SHM_SNAPSHOT_DISPOSABLE_20261030.md` (fixtures uniquement).
- **R3/R4** : SHARED et WAL/SHM standard Win32 sur fixtures, **R3/R4 production NOT_PROVEN**. Nouveau témoin R4 : VFS R3 sans `xShm*` doit REFUSER WAL NORMAL sur SQLite inventée. 268/7/55/165 ATTENDUS NON QUALIFIÉS ; voir `M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md`. PR #215/#35 DRAFT.

## Interdictions actives — STOP

**M3.2 IN_PROGRESS_NOT_ACCEPTED ; writer/R1–R9 NOT_PROVEN ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE.** Historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`. D3b-4/5 et D3b-5 STOP ; D3c conception seulement.

Ne toucher ni aux données opérateur v6/v7 ni aux journaux/sauvegardes ; aucun IPC writer, migration 007, Windows Hello natif, marqueur persistant ou recovery. Dépôt local : `M:\Fabulaxiom` ; profil existant `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1` : aucun accès.

## Prochaines opérations

1. Vérifier postmain #242, puis qualification CI exact-head de la candidature, diff/reviews/threads, Protect main strict bypass=[], squash `expected_head_sha` si admissible, postmain indépendante et #38 append-only.
2. Continuer **P1, R2/R3, R4 xShm*/WAL/SHM/FileId128**, puis R5/R6/R8 et R7/R9 sur fixtures neuves sans promotion production.
3. Actualiser les deux prompts, handoffs et roadmaps à chaque PR.

Références R4 historiques : `M3_2_R4_D3A_LIVE_SHM_FILEID_DISPOSABLE_20261030.md`.

## Documents d'autorité

Lire d'abord [RESUME_PROMPT.md](RESUME_PROMPT.md), puis `HANDOFF_CURRENT.json`, `HANDOFF_CURRENT.md`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Qualification : [M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md](../qualification/M3_2_R4_NO_XSHM_NORMAL_WAL_READ_REFUSAL_DISPOSABLE_20261030.md).

**Règle :** fixtures et anciennes CI ne valent jamais admission de données réelles ; archives dans prompt complet et handoffs.
