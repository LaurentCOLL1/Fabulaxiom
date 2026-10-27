# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**27 octobre — PR192 MERGED :** source `a061311a4d8ca54b213d134c2affa34defa3f023`, CI #40474849956 SUCCESS (147 Rust, 28 gardes, 122 contrats), squash `main=0584291d6dc3c8d2fc8860c8c5084250f4c43ba4`, postmain #40476232974 SUCCESS ; issue #38 terminal 6437767007. [Qualification #192](../qualification/M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md). **Candidate NON qualifiée :** [handoff Windows tenu, parent remplaçable](../qualification/M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md) : 149 Rust, 30 gardes, 123 contrats attendus ; **test-only**. Identité racine/ancêtres et handoff non substituable PAS prouvés ; pas d'ouvreur Tauri. **PR191** postmain #40470700689 SUCCESS ; [persistance v7](../qualification/M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md) ; **PR190** postmain #40462274918 SUCCESS ; **PR189** postmain #40456835489 SUCCESS. [Audit #35](../qualification/M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md) OPEN/DRAFT.

**PR188 :** CI #40450684268 / postmain #40451602743 SUCCESS ; [refus de provenance](../qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md). Archivage 5/5 `OWNER_REPORTED_PASS` non indépendant.

**Windows :** code `M:\Fabulaxiom` (`src`, `src-tauri`, `tools`, `docs`, `.github\workflows`, `src-tauri\target\debug`) ; SQLite neuve hors Git `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3`. Carte `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md`. Historiques privés. PR183 40310982760 / PR184 40338104050.

**Suite :** qualifier la nouvelle CI du handoff Windows témoin, puis prouver propriété/identité de tous les ancêtres et absence de substitution avant tout véritable ouvreur/CRUD/UX v7 dans **le même profil**, sans fichier actif touché. Prospective SOLO non garantie.

**CI historiques (non transférables) :** 40085871815 40094464488 40095354727 40103615181 40106296690 40108674282 40116658246 40122346098 40128407418 40156277835 40169967245 40179336243 40190429389 40200127549 40210737724 40213790809 40220215000 40230066592 40392826209 40403984550 40445392523. B0/B1 propriétaire, consentements consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`.

**Dossiers historiques :** `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` ; `M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md`.

**Runner CI :** Linux `--target` STOP `atk`/`winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; ni compilation ni Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures seulement : CI exacte, diff/reviews/threads, fusion protégée `expected_head_sha`, postmain indépendante. **À chaque PR : les deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider tout nouveau SHA/CI. Aucun accès automatique au Windows de l'opérateur.
