# Fabulaxiom — prompt de reprise COURT (à copier dans une nouvelle discussion)

**Usage :** copie uniquement le texte entre les deux lignes de séparation ci-dessous dans un nouveau chat ChatGPT. **Ce fichier est le point d'entrée court**, maintenu dans chaque PR ; le [prompt de reprise détaillé](RESUME_PROMPT.md) reste la référence longue.

---

Reprends immédiatement et méthodiquement Fabulaxiom depuis son GitHub vivant : https://github.com/LaurentCOLL1/Fabulaxiom

Avant toute action, re-fetch `main`, PR, issues, CI et ruleset `Protect main`. Lis **d'abord le prompt détaillé** `docs/continuity/RESUME_PROMPT.md`, puis `HANDOFF_CURRENT.md`, `HANDOFF_CURRENT.json`, `HANDOFF_PROTOCOL.md`, `HANDOFF_HISTORY.md`, `STATE.md`, `NEXT.md`, `M3_2_GATE_DECISION_CURRENT.md` et `docs/roadmap/ROADMAP_STATUS_CURRENT.md` / `FABULAXIOM_ROADMAP_V1.md`. Ces fichiers GitHub sont l'autorité documentaire ; l'état GitHub actuel prime sur tous les SHA historiques.

**Checkpoint du 24 octobre 2026 :** PR #162 **MERGED**, `main=b5d97648cc18597b23f9fece67fd78b094743abb` ; CI source #40085001106 et postmain #40085871815 **SUCCESS** séparément (78 étapes Windows, 96 contrats, 96 Vitest fictifs, Chromium 82/82 chacun des deux modes, Rust 132). Audit du graphe Windows = 247 dépendances, aucune GTK/GLib sélectionnée pour cette cible ; **cela ne corrige pas glib Linux**. Candidate source-only : vérifier en CI le graphe Cargo `x86_64-unknown-linux-gnu` et constater `glib 0.18.5`/`gtk 0.18.2`/`webkit2gtk 2.0.2`, sans compilation Linux ni accès opérateur, ni changement de `Cargo.lock`, ni dismissal. Contrat #97 ; 79 étapes Windows candidates, nouvelle CI exact HEAD avant fusion protégée. Issue #160 suit les 6 alertes initiales ; Vite 8.1.6 vise 5 alertes npm mais leur fermeture effective reste à lire sur le panneau privé Dependabot.

**Précision runner CI :** le runner Windows ne dispose pas initialement de l'archive du crate Linux `atk 0.18.2`. Un `cargo fetch --locked --target x86_64-unknown-linux-gnu` est donc requis **sur le runner GitHub seulement**, avant `cargo tree --locked --offline` : téléchargement de sources avec checksums de `Cargo.lock`, **sans compilation, sans script, sans écriture d'un nouveau verrou ni contact avec le Windows de l'opérateur**. Le premier run de cette candidate a STOP par absence d'archives offline ; aucun résultat antérieur n'est réutilisable.

**STOP réels :** M3.2 `IN_PROGRESS_NOT_ACCEPTED` ; G2B `NOT_ACCEPTED` ; écrivain `NOT_PROVEN` ; G2C `NOT_AUTHORIZED` ; G3 `STOP_UNAVAILABLE` ; historique `PENDING_EXTERNAL_ATTESTATION(21/3/2)` ; prospective `NOT_STARTED` ; PR #35 OPEN/DRAFT. Ne pas toucher aux SQLite originales v6/v7, backups, ACL, journaux, marqueur, migration 007 ou IPC writer sans autorisation distincte.

Continue sans inventer d'autorisation : travail source-only/fixtures inventées, CI terminale sur SHA exact, contrôle diff/reviews/threads et fusion protégée `expected_head_sha`. **À chaque PR**, actualise ensemble ce prompt court et `RESUME_PROMPT.md`, les deux handoffs et la roadmap/continuité pertinente. Note les résultats terminaux dans l'issue #38 sans réécrire les checkpoints antérieurs. Parallélise uniquement les travaux indépendants.

---

**Note :** ce checkpoint décrit l'état connu lors de la rédaction de la PR documentaire. Une fusion ou CI survenue depuis doit être revalidée et consignée dans une PR ultérieure. Pas d'accès automatique à l'ordinateur de l'opérateur.
