# Fabulaxiom — reprise COURTE

---

Dépôt vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Re-fetch `main`, PR, issues, CI et `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Autorité : GitHub vivant avant les SHA historiques.

**PR199 MERGED :** source `debc6f9cea8ba668f64afd9c815445c282c842c4`, CI #40576413834 SUCCESS (171 Rust/7 Greenfield/36 gardes/130 contrats), `main=4e04412b1d4cbdb4ce738b32c8a06c2ab6127b61`, postmain #40578342548 SUCCESS, issue #38 terminale 6453334855. Six tests HWND fictifs ; aucun Hello natif/PIN/compte/IPC. FileId128 post-`xOpen` NON atomique ; writer NON PROUVÉ. #35 OPEN/DRAFT.

**Candidate NON QUALIFIÉE :** [VFS pré-`xOpen`](../qualification/M3_2_SQLITE_VFS_PREDELEGATION_REFUSAL_FIXTURE_20261027.md), 3 tests Windows jetables ; 174 Rust/7 Greenfield/37 gardes/131 contrats ATTENDUS. Aucun VFS runtime/atomicité ; Hello natif NON AUTORISÉ.

**Historique :** PR198 `34b4174dd79d7c133b3700d72a705236f7623640` / #40571697037 ; [HWND](../qualification/M3_2_WINDOWS_HELLO_DESKTOP_HWND_BACKEND_BOUNDARY_20261027.md) ≥22000. PR197 main=dde962a50e3a063753fb77e9a5bcee014f406d30 / #40558476584, [Hello](../qualification/M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md). PR196 #40525427034, PR195 #40518270685, PR194 #40508416842 ; négatifs #40499869627/#40501278786.

**PR188 :** CI #40450684268 / postmain #40451602743 SUCCESS ; [provenance](../qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md). Archivage 5/5 `OWNER_REPORTED_PASS`, non indépendant.

**Sources :** `M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md`, `M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md`, `M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md`, `M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md`, `M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md`, `M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md`. Postmain PR189–193 : 40456835489 40462274918 40470700689 40476232974 40486676658.

**Windows :** `M:\Fabulaxiom` ; SQLite neuve `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3`, hors Git. Carte `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md` ; historiques privés. PR183 40310982760 / PR184 40338104050.

**Suite :** Hello natif NON AUTORISÉ ; atomicité SQLite/writer avant CRUD v7. [#35](../qualification/M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md), SOLO incertain.

**CI historiques (non transférables) :** 40085871815 40094464488 40095354727 40103615181 40106296690 40108674282 40116658246 40122346098 40128407418 40156277835 40169967245 40179336243 40190429389 40200127549 40210737724 40213790809 40220215000 40230066592 40392826209 40403984550 40445392523. B0/B1 consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`.

**Archives :** `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` ; `M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md`.

**Runner :** Linux `--target` STOP `atk`/`winapi`. CI : `cargo fetch --locked` sans `--target`, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu`.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures : CI exacte, diff/reviews/threads, `expected_head_sha`, postmain indépendante. **Chaque PR : deux prompts, deux handoffs, roadmap, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider SHA/CI. Pas d'accès Windows opérateur.
