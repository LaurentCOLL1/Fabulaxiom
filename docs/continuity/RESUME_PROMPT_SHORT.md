# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**26 octobre — PR183 MERGED :** source `7879f2b052944d68ca367537809b0af8e05bca04` CI #40309445029 SUCCESS ; squash `main=39725a020a8656b8d0488628bc208fcf104c058c`, postmain #40310982760 SUCCESS indépendante. **Voie C projets neufs uniquement :** Windows Tauri dev `com.fabulaxiom.greenfield.v1` lancé, archivage de révisions **5/5 OWNER_REPORTED_PASS** (masquer, afficher/texte intact, désarchiver, persister après relance, protéger courante), sans preuve indépendante : [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6417653782). Préférences `app_metadata` v6, aucune suppression de texte ; CI anciennes non transférables.

**Dossiers Windows :** `M:\Fabulaxiom` Git/code ; `M:\Fabulaxiom\src` React ; `M:\Fabulaxiom\src-tauri` Rust/Tauri ; `M:\Fabulaxiom\tools` scripts ; `M:\Fabulaxiom\docs\continuity` prompts ; `M:\Fabulaxiom\docs\roadmap` ; `M:\Fabulaxiom\.github\workflows` CI ; `M:\Fabulaxiom\src-tauri\target\debug` exécutable dev. **Hors Git :** `%LOCALAPPDATA%\com.fabulaxiom.greenfield.v1\database\fabulaxiom.sqlite3` (neuve). Carte : `docs/continuity/WINDOWS_OPERATOR_PATHS_ROUTE_C_20261026.md`. Historiques : emplacements privés non publiés.

**Suite :** sauvegarde/restauration sûre des **nouveaux projets** en fixtures/CI d'abord ; ne rien écraser sur le poste. Toute commande PowerShell doit être entièrement encapsulée dans `& { ... }`.

**25 octobre (historique) :** PR169–177 postmain 40128407418, 40156277835, 40169967245, 40179336243, 40190429389, 40200127549, 40210737724, 40213790809, 40220215000 SUCCESS ; PR178 #40229362824/#40230066592 SUCCESS. `toy_26` double lecture sale ≠ commit. B0 M1.5=4 noms/M2.5=1, B1 RESTORED vers un nom, déclarés par le propriétaire seulement ; consentements consommés. A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`, C `DEVELOPMENT_ONLY`.

**24 octobre :** PR168 CI #40117705107/#40122346098 SUCCESS ; observations G2A/B0/B1 et six copies ≠ attestation indépendante.

**CI historiques à préserver :** #40085871815, #40094464488, #40095354727, #40103615181, #40106296690, #40108674282, #40116658246. Anciennes CI non transférables au HEAD nouveau.

**Runner CI :** preload Linux `--target` a STOP sur `atk` puis `winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; sources verrouillées uniquement, sans compilation ni contact avec Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Source/fixtures seulement : CI exacte, diff/reviews/threads, fusion protégée `expected_head_sha`, postmain indépendante. **À chaque PR : les deux prompts, deux handoffs, roadmap/continuité, issue #38 append-only.**

---

**Note :** checkpoint daté ; revalider tout nouveau SHA/CI. Aucun accès automatique au Windows de l'opérateur.
