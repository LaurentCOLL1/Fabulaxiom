# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**27 octobre — PR186 MERGED :** source `ad202a0310c378bdbda430f68d9d8686f59a6e18` CI #40402322000 SUCCESS ; squash `main=92160c6401fa8b9f2f1667704fb8f51294fdae72`, postmain #40403984550 SUCCESS indépendante ; issue #38 commentaire 6427938179. 140 Rust, 4/4 Greenfield, 116 contrats. PR185 postmain #40392826209 historique. Windows Tauri DEV **PROJETS NEUFS** `com.fabulaxiom.greenfield.v1` fonctionne ; archivage 5/5 `OWNER_REPORTED_PASS` non indépendant (issue #38 commentaire 6417653782), préférences `app_metadata` v6, textes immuables.

**Windows :** `M:\Fabulaxiom` Git/code ; sous-dossiers `src` React, `src-tauri` Rust/Tauri, `tools`, `docs\continuity`, `docs\roadmap`, `.github\workflows` CI ; `src-tauri\target\debug` build dev. **Hors Git :** `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3` (neuve). Carte : `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md`. Historiques privés. PR183 postmain 40310982760 / PR184 40338104050 historiques.

**Suite candidate :** `docs/qualification/M3_2_ROUTE_C_SAME_PROFILE_RESTORE_REFUSAL_20261027.md` : corruption de sauvegarde **refusée dans le même profil de fixture**, marqueur et anciens fichiers préservés ; 5 Rust Greenfield / 7 gardes / 117 contrats **à qualifier sur nouvelle CI**. Précédents : `M3_2_ROUTE_C_SAME_PROFILE_RESTORE_20261026.md`, `M3_2_ROUTE_C_GREENFIELD_BACKUP_RESTORE_20261026.md`. **Ne jamais recréer le profil opérateur** : restauration valide = nouveau fichier SQLite dans le même profil, ancien conservé. Aucun geste opérateur ; PowerShell dans `& { ... }`.

**25 octobre (historique) :** PR169–178 postmain 40128407418, 40156277835, 40169967245, 40179336243, 40190429389, 40200127549, 40210737724, 40213790809, 40220215000, 40230066592 SUCCESS. `toy_26` double lecture sale ≠ commit. B0 M1.5=4 noms/M2.5=1, B1 RESTORED vers un nom, propriétaire seul ; consentements consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`, C `DEVELOPMENT_ONLY`.

**24 octobre :** PR168 #40117705107/#40122346098 SUCCESS ; G2A/B0/B1 et six copies ≠ attestation.

**CI historiques à préserver :** #40085871815, #40094464488, #40095354727, #40103615181, #40106296690, #40108674282, #40116658246. Anciennes CI non transférables au HEAD nouveau.

**Runner CI :** Linux `--target` STOP `atk`/`winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; ni compilation ni Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures seulement : CI exacte, diff/reviews/threads, fusion protégée `expected_head_sha`, postmain indépendante. **À chaque PR : les deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider tout nouveau SHA/CI. Aucun accès automatique au Windows de l'opérateur.
