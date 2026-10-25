# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**25 octobre 2026 :** PR169–PR177 postmain SUCCESS : #40128407418, #40156277835, #40169967245, #40179336243, #40190429389, #40200127549, #40210737724, #40213790809, #40220215000. PR177 source `32093f7f31f26c98e7b91bc9d25930ee4f973d27` CI #40219228723 SUCCESS (81/81 Windows) ; squash `main=c1868256739247810ecf6b606e051b53b8c0d529` postmain #40220215000 `push/SUCCESS` indépendante (80 SUCCESS, 1 SKIPPED ; 111 contrats, 96 Vitest fictifs, Chromium 82/82 x2, 132 Rust, `toy_24`/`toy_25` PASS). [Checkpoint terminal #38](https://github.com/LaurentCOLL1/Fabulaxiom/issues/38#issuecomment-6401436944). Dirty reads en RAM et `ROLLBACK` sans `data_version` : non-attestation. **Prochain candidat `toy_26`** : deux lectures sales identiques malgré `query_only`, `total_changes` et `data_version` locaux stables ; aucune CI candidate anticipée. G2B0 M1.5=4/M2.5=1 noms, B1 RESTORED vers un nom : `OBSERVED_PARTIAL_ONLY_OWNER_REPORTED`, consentements consommés. Route A `UNAVAILABLE_NOT_PROVEN`, B `NOT_PROVEN`, C fiction ; STOP ci-dessous.

**Checkpoint du 24 octobre 2026 (historique) :** PR168 MERGED `main=a03cc5dad68aaf4cb78c39520de130960dc565f8`, source `d1f6db636a09112ace772b734c1a33e81d63d168`, CI source #40117705107 / postmain #40122346098 SUCCESS séparément (79 Windows, 102 contrats, 96 Vitest, Chromium 82/82 x2, 132 Rust). G2-A métadonnées OWNER_REPORTED ; B0 proposition dans `docs/qualification/M3_2_G2B0_METADATA_ONLY_OPERATOR_REVIEW_20261024.md`, autorisation locale distincte alors requise et depuis consommée ; deux racines connues, aucune SQLite ouverte. Six copies récupérées sans attestation historique indépendante.

**CI historiques à préserver :** #40085871815, #40094464488, #40095354727, #40103615181, #40106296690, #40108674282, #40116658246. Anciennes CI non transférables au HEAD nouveau.

**Runner CI :** preload Linux `--target` a STOP sur `atk` puis `winapi`. Sur GitHub jetable : `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu` ; sources verrouillées uniquement, sans compilation ni contact avec Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Continue sans inventer d'autorisation : travail source-only/fixtures inventées, CI terminale sur SHA exact, contrôle diff/reviews/threads et fusion protégée `expected_head_sha`. **À chaque PR**, actualise ensemble ce prompt court et `RESUME_PROMPT.md`, les deux handoffs et la roadmap/continuité pertinente. Note les résultats terminaux dans l'issue #38 sans réécrire les checkpoints antérieurs. Parallélise uniquement les travaux indépendants.

---

**Note :** ce checkpoint décrit l'état connu lors de la rédaction de la PR documentaire. Une fusion ou CI survenue depuis doit être revalidée et consignée dans une PR ultérieure. Pas d'accès automatique à l'ordinateur de l'opérateur.
