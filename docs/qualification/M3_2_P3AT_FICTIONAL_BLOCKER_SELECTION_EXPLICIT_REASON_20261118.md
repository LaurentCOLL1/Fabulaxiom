# P3at — sélection de révocation fictive avec motif indépendant (18 novembre 2026)

## Règle produit
Depuis les liens humains bloquants affichés par P3as, « Préparer la révocation » sélectionne le lien exact sans changer le brouillon ni son audit. La révocation requiert toujours une action séparée, un nouveau motif humain dédié (jamais repris automatiquement du formulaire de création), et conserve le lien révoqué dans l'historique. Toute sélection efface le motif de révocation antérieur ; refus sans motif = zéro mutation et revue précédente invalidée.

## Preuves candidates
Vitest #37 : refus sans motif propre, audit inchangé, révocation explicitement justifiée inscrite en RAM ; étiquette de motif indépendant. Chromium #107 : sélection directe de `human-ab` sans mutation, refus si aucun motif dédié même si celui de création est rempli, puis révocation volontaire avec motif dédié, audit fictif `precedence_revoked`. Attendu 107/107 et CSP strict : **NON QUALIFIÉ** jusqu'à CI Windows source HEAD exacte.

## Gate et provenance
Parent protected `main=eaa9965dd80617fe1989eeaa9631126b08eb937a` après #387 MERGED, CI source #44225434422 completed/SUCCESS au HEAD `32dce29ac3b0b8bcff9c04de897e71aabad3a7b4`, postmain indépendante #44235808595 completed/SUCCESS au SHA parent exact. Protect main ACTIVE strict bypass=[]. Diff/reviews/threads, CI source SHA exact, guarded squash expected_head_sha, postmain indépendante, #38 append-only requis avant admission. Checklist 104=9 closes/95 ouvertes ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% indicatif).

## STOP
PRODUCT_FIRST_PARALLEL_SAFETY. Atelier React RAM fictif non monté, sans production/writer, Tauri IPC, SQLite réel, migration, backup, Hello ou recovery. Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP, R3 partiel, D3c conception, D3b-4/5 et D3b-5 STOP ; main/WAL/SHM/live WAL-index/ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
