# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**Checkpoint du 24 octobre 2026 :** PR #167 **MERGED**, `main=533bdb27480a2b6dbed630b148501eeaf3c34b1e` ; source `819dbb0a1d80a07e9c19b3e7eacff761dce8dc9b`, CI source #40115530223 et postmain #40116658246 **SUCCESS indépendamment** (79 Windows, 101 contrats, 96 Vitest fictifs, Chromium 82/82 par mode, Rust 132). La **copie privée détachée** M2.5 a été contrôlée uniquement en RAM : `integrity_check=ok`, FK 0, 14 tables, migrations 1..6, effectifs M2.5 compatibles. **Ce n'est pas une preuve d'identité historique**. Candidate : documentation G2 SOLO non exécutable, 102e contrat et CI neuve requise. Copie/empreintes privées hors GitHub ; G2B et G3 restent STOP, prospective NOT_STARTED ; issue #36 cinq témoins non attestés, issue #38 gouverne la suite.

**CI historiques à préserver (#97–#101) :** #40085871815, #40094464488, #40095354727, #40103615181, #40106296690, #40108674282. Aucune de ces CI ne qualifie un nouveau HEAD.

**Précision runner CI :** le préchargement limité à Linux a STOP sur `atk`, puis `winapi`. La correction qualifiée sur runner GitHub jetable utilise `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu`. Cela télécharge uniquement des sources vérifiées par le verrou, ne compile rien et ne contacte pas le Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Continue sans inventer d'autorisation : travail source-only/fixtures inventées, CI terminale sur SHA exact, contrôle diff/reviews/threads et fusion protégée `expected_head_sha`. **À chaque PR**, actualise ensemble ce prompt court et `RESUME_PROMPT.md`, les deux handoffs et la roadmap/continuité pertinente. Note les résultats terminaux dans l'issue #38 sans réécrire les checkpoints antérieurs. Parallélise uniquement les travaux indépendants.

---

**Note :** ce checkpoint décrit l'état connu lors de la rédaction de la PR documentaire. Une fusion ou CI survenue depuis doit être revalidée et consignée dans une PR ultérieure. Pas d'accès automatique à l'ordinateur de l'opérateur.
