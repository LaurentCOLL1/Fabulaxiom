# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**26 octobre 2026 :** PR182 CI #40282690233/#40283775120 `SUCCESS` indépendants, `main=91da6b5ef3b55c702dcd18aead27ce2df3b0b9b0`. PR181 `main=06452e2ae7e442272a6c1429b1454f56f2266d57`, CI #40277924539/#40278919705 SUCCESS historiques. **Voie C : projets neufs uniquement.** Windows opérateur : préflight, fenêtre « PROJETS NEUFS », pont React→Tauri→Rust, SQLite v6 et persistance après réouverture **OWNER_REPORTED_PASS**, sans témoin indépendant (issue #38). Nouvelle candidate : **masquer/archiver réversiblement les révisions** dans l'identité Tauri Greenfield, préférences `app_metadata` v6 sans migration 007 ni suppression des révisions. `docs/qualification/M3_2_ROUTE_C_REVISION_ARCHIVE_20261026.md`. Nouvelle PR exige CI SHA exact et postmain ; aucun G2/G3/release.

**25 octobre 2026 (historique) :** PR169–177 postmain 40128407418, 40156277835, 40169967245, 40179336243, 40190429389, 40200127549, 40210737724, 40213790809, 40220215000 SUCCESS ; PR178 source PR178 #40229362824 et postmain #40230066592 SUCCESS séparément sur leurs SHA (112 contrats, 96 Vitest fictifs, Chromium 82/82 ×2, 132 Rust). `toy_26` : double lecture sale stable ≠ commit. B0 quatre noms M1.5/un M2.5 ; B1 marqueur RESTORED vers un nom, compte rendu propriétaire uniquement ; consentements consommés. Routes A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`, C `DEVELOPMENT_ONLY`. Détails, SHA et résultats dans le prompt long et l'historique.

**24 octobre (historique) :** PR168, CI #40117705107/#40122346098 SUCCESS. G2A/B0/B1 OWNER_REPORTED et consentements consommés, aucune SQLite ouverte. Six copies ≠ attestation indépendante.

**CI historiques à préserver :** #40085871815, #40094464488, #40095354727, #40103615181, #40106296690, #40108674282, #40116658246. Anciennes CI non transférables au HEAD nouveau.

**Runner CI :** preload Linux `--target` a STOP sur `atk` puis `winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; sources verrouillées uniquement, sans compilation ni contact avec Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Continue sans inventer d'autorisation : travail source-only/fixtures inventées, CI terminale sur SHA exact, contrôle diff/reviews/threads et fusion protégée `expected_head_sha`. **À chaque PR**, actualise ensemble ce prompt court et `RESUME_PROMPT.md`, les deux handoffs et la roadmap/continuité pertinente. Note les résultats terminaux dans l'issue #38 sans réécrire les checkpoints antérieurs. Parallélise uniquement les travaux indépendants.

---

**Note :** ce checkpoint décrit l'état connu lors de la rédaction de la PR documentaire. Une fusion ou CI survenue depuis doit être revalidée et consignée dans une PR ultérieure. Pas d'accès automatique à l'ordinateur de l'opérateur.
