# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**27 octobre — PR191 MERGED :** source `c6b23ae071392c5f68912e53915df5067787605b`, CI #40469481613 SUCCESS (144 Rust), squash `main=2b4a7aaa37b2ada590a8e05fc4c5e973949041cc`, postmain #40470700689 SUCCESS ; issue #38 terminal 6436913166. **Candidate nouvelle NON qualifiée :** [réservation exclusive de SQLite v7 neuve, refus des fichiers/dossiers/sidecars occupés et deux créateurs simultanés](../qualification/M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md) : 3 Rust, 28 gardes, 122 contrats attendus ; **test-only**, pas d'ouvreur Tauri ni protection de course hostile prouvée. **PR190 historique** postmain #40462274918 SUCCESS ; [persistance v7](../qualification/M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md). **PR189** postmain #40456835489 SUCCESS. [Audit #35](../qualification/M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md) OPEN/DRAFT, pas de merge.

**Historique PR188 :** CI #40450684268, postmain #40451602743 SUCCESS ; [refus de provenance de sauvegarde](../qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md), tests Greenfield transférables uniquement à leur SHA. Archivage 5/5 `OWNER_REPORTED_PASS` non indépendant.

**Windows :** `M:\Fabulaxiom` code (`src`, `src-tauri`, `tools`, `docs`, `.github\workflows`, `src-tauri\target\debug`) ; SQLite neuve hors Git : `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3`. Carte : `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md`. Historiques privés. PR183 postmain 40310982760 / PR184 40338104050.

**Suite :** qualifier l'exclusivité CI ; puis propriété racine et handoff sans substitution, véritable ouvreur/CRUD/UX v7 dans **même profil** sans fichiers actifs touchés. Prospective SOLO non garantie.

**CI historiques :** 40085871815 40094464488 40095354727 40103615181 40106296690 40108674282 40116658246 40122346098 40128407418 40156277835 40169967245 40179336243 40190429389 40200127549 40210737724 40213790809 40220215000 40230066592 40392826209 40403984550 40445392523 ; non transférables. B0/B1 propriétaire seul ; consentements consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`.

**Dossiers historiques :** `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` ; `M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md`.

**Runner CI :** Linux `--target` STOP `atk`/`winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; ni compilation ni Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures seulement : CI exacte, diff/reviews/threads, fusion protégée `expected_head_sha`, postmain indépendante. **À chaque PR : les deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider tout nouveau SHA/CI. Aucun accès automatique au Windows de l'opérateur.
