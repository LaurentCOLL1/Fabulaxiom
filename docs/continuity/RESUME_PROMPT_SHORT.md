# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**Checkpoint du 24 octobre 2026 :** PR #165 **MERGED**, `main=e1faacc909d4c8a693e2552e64dda57b6927473f` ; source `1c592c76c48feba3ef3f5e11fca37bb0efaba03f`, CI source #40105412509 et postmain #40106296690 **SUCCESS indépendamment** (79 étapes Windows, 99 contrats, 96 Vitest fictifs, Chromium 82/82 dans chaque mode, Rust 132). Premier run source #40105270459 FAILURE sur un ancien SHA : non réutilisé. **Candidate** : refuser les doublons de références/hachages de *notices fictives* dans l'intake historique, sans produire de preuve réelle (100e contrat et CI neufs exigés). Issue #36 : cinq témoins manquants. Issue #160 : `glib 0.18.5` dans graphe Linux (277 paquets), `OPEN_NOT_REMEDIATED`, npm Vite 8.1.6 ciblé, clôture Dependabot privée non prouvée.

**Références historiques préservées pour contrats #97–#99 :** PR #162 CI postmain #40085871815 ; PR #163 CI source #40094464488 et postmain #40095354727 ; PR #164 CI postmain #40103615181. Ces anciennes CI ne qualifient jamais un nouveau HEAD.

**Précision runner CI :** le préchargement limité à Linux a STOP sur `atk`, puis `winapi`. La correction qualifiée sur runner GitHub jetable utilise `cargo fetch --locked` **sans `--target`**, puis `cargo tree --locked --offline --target x86_64-unknown-linux-gnu`. Cela télécharge uniquement des sources vérifiées par le verrou, ne compile rien et ne contacte pas le Windows opérateur.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Continue sans inventer d'autorisation : travail source-only/fixtures inventées, CI terminale sur SHA exact, contrôle diff/reviews/threads et fusion protégée `expected_head_sha`. **À chaque PR**, actualise ensemble ce prompt court et `RESUME_PROMPT.md`, les deux handoffs et la roadmap/continuité pertinente. Note les résultats terminaux dans l'issue #38 sans réécrire les checkpoints antérieurs. Parallélise uniquement les travaux indépendants.

---

**Note :** ce checkpoint décrit l'état connu lors de la rédaction de la PR documentaire. Une fusion ou CI survenue depuis doit être revalidée et consignée dans une PR ultérieure. Pas d'accès automatique à l'ordinateur de l'opérateur.
