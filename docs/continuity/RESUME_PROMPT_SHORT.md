# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

---

Dépôt vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**27 octobre — PR196 MERGED :** source `2925a6a561f54fe3e7c0dc9aa7301e6a1c55930a`, CI #40523209147 SUCCESS (154 Rust/35 gardes/127 contrats), `main=3546e62a19cb4db0da970cb07019982ff6c8634a`, postmain #40525427034 SUCCESS, issue #38 6445506535. FileId128 **post-`xOpen`**, aucune atomicité. **Décision Laurent : mono-utilisateur, Windows Hello pour opérations sensibles ; aucun compte/mot de passe Fabulaxiom.** [Candidate NON QUALIFIÉE](../qualification/M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md) : 11 Rust `#[cfg(test)]`, one-shot et refus ; **165 Rust/36 gardes/128 contrats attendus**. Hello/PIN/IPC/SQLite opérateur NON activés. PR195 #40518270685 ; PR194 #40508416842 ; échecs #40499869627/#40501278786. #35 OPEN/DRAFT.

**PR188 :** CI #40450684268 / postmain #40451602743 SUCCESS ; [refus de provenance](../qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md). Archivage 5/5 `OWNER_REPORTED_PASS` non indépendant.

**Sources précédentes :** `M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md`, `M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md`, `M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md`, `M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md`, `M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md`, `M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md`. CI postmain PR189–193 : 40456835489 40462274918 40470700689 40476232974 40486676658 (historique).

**Windows :** code `M:\Fabulaxiom` ; SQLite neuve hors Git `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3`. Carte `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md`. Historiques privés. PR183 40310982760 / PR184 40338104050.

**Suite :** qualifier Hello test-only ; atomicité SQLite à prouver avant CRUD/UX v7 **même profil**. [Audit #35](../qualification/M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md), SOLO non garantie.

**CI historiques (non transférables) :** 40085871815 40094464488 40095354727 40103615181 40106296690 40108674282 40116658246 40122346098 40128407418 40156277835 40169967245 40179336243 40190429389 40200127549 40210737724 40213790809 40220215000 40230066592 40392826209 40403984550 40445392523. B0/B1 consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`.

**Dossiers historiques :** `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` ; `M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md`.

**Runner CI :** Linux `--target` STOP `atk`/`winapi`. GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; pas de compilation Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures seulement : CI exacte, diff/reviews/threads, fusion protégée `expected_head_sha`, postmain indépendante. **À chaque PR : les deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider tout nouveau SHA/CI. Aucun accès automatique au Windows de l'opérateur.
