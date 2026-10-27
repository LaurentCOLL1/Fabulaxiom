# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**27 octobre — PR195 MERGED :** source `f84f3035170baa4830879796230675ad8b328a2c`, CI #40516204731 SUCCESS (**153 Rust, 7 Greenfield, 34 gardes, 126 contrats**), `main=1ab320f7834086ac587ce2fdaa8638d7c29d61f5`, postmain #40518270685 SUCCESS, issue #38 6444458042. **Candidate NON QUALIFIÉE :** [FileId 128 et Windows Hello](../qualification/M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md) : **154 Rust / 35 gardes / 127 contrats attendus**. Hello **non implémenté**, son consentement ne prouve ni atomicité SQLite ni absence de writer. PR194 postmain #40508416842, échecs Win32 #40499869627 / #40501278786 ; PR193 #40486676658 ; PR192 #40476232974 ; PR191 #40470700689 ; PR190 #40462274918 ; PR189 #40456835489 SUCCESS. [audit #35](../qualification/M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md) OPEN/DRAFT.

**PR188 :** CI #40450684268 / postmain #40451602743 SUCCESS ; [refus de provenance](../qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md). Archivage 5/5 `OWNER_REPORTED_PASS` non indépendant.

**Sources précédentes :** `M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md`, `M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md`, `M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md`, `M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md`, `M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md`.

**Windows :** code `M:\Fabulaxiom` (`src`, `src-tauri`, `tools`, `docs`) ; SQLite neuve hors Git `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3`. Carte `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md`. Historiques privés. PR183 40310982760 / PR184 40338104050.

**Suite :** qualifier FileId 128 sur runner puis traiter l'atomicité avant tout ouvreur/CRUD/UX v7 dans **le même profil**. Prospective SOLO non garantie.

**CI historiques (non transférables) :** 40085871815 40094464488 40095354727 40103615181 40106296690 40108674282 40116658246 40122346098 40128407418 40156277835 40169967245 40179336243 40190429389 40200127549 40210737724 40213790809 40220215000 40230066592 40392826209 40403984550 40445392523. B0/B1 propriétaire, consentements consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`.

**Dossiers historiques :** `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` ; `M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md`.

**Runner CI :** Linux `--target` STOP `atk`/`winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; ni compilation ni Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures seulement : CI exacte, diff/reviews/threads, fusion protégée `expected_head_sha`, postmain indépendante. **À chaque PR : les deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider tout nouveau SHA/CI. Aucun accès automatique au Windows de l'opérateur.
