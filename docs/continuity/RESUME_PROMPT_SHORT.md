# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**25 octobre 2026 — checkpoint vérifié après PR #169 :** source `67e2b400510fe4bade797a9fd73997f892ded1ad` et CI [#40127450956](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40127450956) SUCCESS ; `main=4ea2c5f9ad380863c5634dae65faac9831b1cec3` et CI postmain indépendante [#40128407418](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/40128407418) SUCCESS au SHA exact, 79 étapes Windows, voir [issue #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6392307076). G2-B0 demeure `PREPARED_NOT_EXECUTED`, sans consentement nouveau.

**Candidat nouveau source-only :** garde AST PowerShell `tools/m32_g2b0_ast_static_review.ps1` sur runner CI jetable : uniquement `Parser.ParseInput`, analyse de forme et 10 refus fictifs, JAMAIS exécution du bloc opérateur. Contrat #104, seuils non encore prouvés : 80 étapes Windows, 104 contrats, 96 Vitest fictifs, Chromium 82/82 deux modes, 132 Rust. Pas une certification de sûreté OS/TOCTOU/absence d'écrivain. Re-fetch main/PR/CI/diff/reviews/threads/ruleset, `expected_head_sha` après CI terminale exacte, puis postmain indépendante.

**STOP inchangés :** M3.2 `IN_PROGRESS_NOT_ACCEPTED`, G2B `NOT_ACCEPTED`, écrivain `NOT_PROVEN`, origine `PARTIAL_LOCAL_IDENTITY_ONLY`, G2C `NOT_AUTHORIZED`, G3 `STOP_UNAVAILABLE`, historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)`, prospective `NOT_STARTED`, PR #35 OPEN/DRAFT. Deux racines M1.5/M2.5 seulement, M3.1 v7 non évalué, aucun accès SQLite originale/backups/ACL/journaux/marker/migration 007/IPC writer ou Windows opérateur.

**Checkpoint du 24 octobre 2026 :** PR #168 MERGED, `main=a03cc5dad68aaf4cb78c39520de130960dc565f8`, source `d1f6db636a09112ace772b734c1a33e81d63d168`. CI source #40117705107 et postmain #40122346098 **SUCCESS indépendamment** : 79 étapes Windows, 102 contrats, 96 Vitest fictifs, Chromium 82/82 par mode, 132 Rust. G2-A PASS métadonnées uniquement selon opérateur ; prochain candidat : bloc G2-B0 metadata-only **à relire, non exécuté, autorisation locale distincte requise** dans `docs/qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md`. Deux racines connues (production M1.5, isolée M2.5), aucune base SQL ouverte ; M3.1 et autres rôles NOT_ASSESSED. Les six copies récupérées et la validation mémoire ne fournissent toujours **aucune attestation indépendante historique**.

**CI historiques à préserver :** #40085871815, #40094464488, #40095354727, #40103615181, #40106296690, #40108674282, #40116658246. Anciennes CI non transférables au HEAD nouveau.

**Précision runner CI :** le préchargement limité à Linux a STOP sur `atk`, puis `winapi`. La correction qualifiée sur runner GitHub jetable utilise `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu`. Cela télécharge uniquement des sources vérifiées par le verrou, ne compile rien et ne contacte pas le Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Continue sans inventer d'autorisation : travail source-only/fixtures inventées, CI terminale sur SHA exact, contrôle diff/reviews/threads et fusion protégée `expected_head_sha`. **À chaque PR**, actualise ensemble ce prompt court et `RESUME_PROMPT.md`, les deux handoffs et la roadmap/continuité pertinente. Note les résultats terminaux dans l'issue #38 sans réécrire les checkpoints antérieurs. Parallélise uniquement les travaux indépendants.

---

**Note :** ce checkpoint décrit l'état connu lors de la rédaction de la PR documentaire. Une fusion ou CI survenue depuis doit être revalidée et consignée dans une PR ultérieure. Pas d'accès automatique à l'ordinateur de l'opérateur.
