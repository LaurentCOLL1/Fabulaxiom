# Fabulaxiom — reprise COURTE

---

Dépôt vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Re-fetch `main`, PR, issues, CI et `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Autorité : GitHub vivant avant les SHA historiques.

**PR201 MERGED :** `c9b8567f6b1a0c4af44a835ec2fe5f39449193e5`, CI #40593808508 SUCCESS (177/7/38/132), `main=d235e492c5081734ff226563eec6fdb983e4808d`, postmain #40595455638 SUCCESS, #38 6455411875. [FileId128](../qualification/M3_2_SQLITE_VFS_FILEID128_PREDISPATCH_TOCTOU_20261027.md) non atomique ; writer `NOT_PROVEN`.

**Candidate NON QUALIFIÉE :** [VFS WAL/SHM](../qualification/M3_2_SQLITE_VFS_WAL_SHM_BOUNDARY_20261028.md), refus `SQLITE_OPEN_WAL` avant délégation ; `-shm` créé via `xShmMap` sans passer par `xOpen`. Deux tests Windows jetables, **179 Rust/7 Greenfield/39 gardes/133 contrats ATTENDUS**, pas PASS. Aucun VFS runtime/CRUD, aucune SQLite opérateur, Hello natif NON AUTORISÉ. #35 OPEN/DRAFT.

**Historique :** PR200 #40584565021/#40586436340 ; PR199 #40578342548 [VFS](../qualification/M3_2_SQLITE_VFS_PREDELEGATION_REFUSAL_FIXTURE_20261027.md) ; PR198 #40571697037 [HWND](../qualification/M3_2_WINDOWS_HELLO_DESKTOP_HWND_BACKEND_BOUNDARY_20261027.md) ≥22000 ; PR197 main=dde962a50e3a063753fb77e9a5bcee014f406d30 / #40558476584 [Hello](../qualification/M3_2_SINGLE_USER_WINDOWS_HELLO_SENSITIVE_CONSENT_POLICY_20261027.md) ; PR196 #40525427034 ; PR195 #40518270685 ; PR194 #40508416842 ; négatifs #40499869627/#40501278786.

**PR188 :** #40450684268 / postmain #40451602743 SUCCESS ; [provenance](../qualification/M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_SCHEMA_REFUSAL_20261027.md). 5/5 `OWNER_REPORTED_PASS` non indépendant.

**Sources :** `M3_2_GREENFIELD_NEW_ONLY_DISPOSABLE_V7_CHRONOLOGY_PERSISTENCE_20261027.md`, `M3_2_GREENFIELD_V7_EXCLUSIVE_NEW_FILE_CLAIM_20261027.md`, `M3_2_GREENFIELD_V7_PINNED_HANDOFF_PARENT_NAMESPACE_20261027.md`, `M3_2_GREENFIELD_V7_OWNED_FIXTURE_DIRECTORY_CHAIN_20261027.md`, `M3_2_GREENFIELD_V7_SQLITE_WIN32_NATIVE_HANDLE_POSTOPEN_20261027.md`, `M3_2_WIN32_FILEID_128_AND_WINDOWS_HELLO_BOUNDARY_20261027.md`. Postmain PR189–193 : 40456835489 40462274918 40470700689 40476232974 40486676658.

**Windows :** `M:\Fabulaxiom` ; SQLite neuve `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3` ; `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md` privé. PR183 40310982760 / PR184 40338104050.

**Suite :** atomicité/writer avant CRUD ; Hello NON AUTORISÉ. [#35](../qualification/M3_2_PR35_LIVE_AUDIT_PROSPECTIVE_FAST_TRACK_20261027.md), SOLO incertain.

**CI historiques (non transférables) :** 40085871815 40094464488 40095354727 40103615181 40106296690 40108674282 40116658246 40122346098 40128407418 40156277835 40169967245 40179336243 40190429389 40200127549 40210737724 40213790809 40220215000 40230066592 40392826209 40403984550 40445392523. B0/B1 consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`.

**Archives :** `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md` ; `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` ; `M3_2_ROUTE_C_SAME_PROFILE_FOREIGN_KEY_RESTORE_REFUSAL_20261027.md`.

**Runner :** Linux `--target` STOP `atk`/`winapi` ; `cargo fetch --locked` sans `--target`, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu`.

**STOP :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, writer `NOT_PROVEN`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, #35 OPEN/DRAFT. SQLite v6/v7, backups, ACL, journaux, marqueur, migration 007, IPC writer interdits sans accord distinct.

Source/fixtures : CI exacte, diff/reviews/threads, `expected_head_sha`, postmain indépendante. **Chaque PR : deux prompts, deux handoffs, roadmap, issue #38 append-only.**

---

**Note :** Windows non accédé.
