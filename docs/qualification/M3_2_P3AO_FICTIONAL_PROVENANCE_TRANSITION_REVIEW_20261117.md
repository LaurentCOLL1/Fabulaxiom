# P3ao — décision explicite sur la provenance fictive (17 novembre 2026)

## Produit et sécurité
La revue d'une correction d'ancre RAM distingue cinq transitions exclusivement calculées depuis des identités de révisions fictives exactes : aucune source (`none`), nouvelle source (`linked`), conservation (`retained`), remplacement (`replaced`) et détachement (`detached`). Les identifiants de scènes, romans et révisions d'origine restent visibles ; aucun titre ni historique n'est inféré. Toute valeur de transition falsifiée dans la prévisualisation fait refuser la confirmation RAM ; les originaux ne changent pas.

## Preuves candidates
Six Vitest #27–32 : cinq transitions et refus d'une décision falsifiée. Chromium #102 : invalidation de l'ancienne revue lorsque la scène et la révision changent, affichage d'une décision différente au nouveau passage. Attendu 102/102 Chromium sous CSP ; **CANDIDAT non qualifié** sans nouvelle CI sur HEAD P3ao exact.

## Limites et gouvernance
Parent protected `main=e23eb98fbf11e18691609266ec7687a2514c0be2`, PR #382 source CI #43956570613 completed/SUCCESS HEAD exact `9b308c9f8dc3add32232933d57894ef5645ad6dd`, postmain #43984047043 completed/SUCCESS SHA exact parent. Seulement atelier fictif React non monté ; aucun SQLite opérateur, writer, Tauri IPC, v6/v7, sauvegarde, Windows Hello ni recovery. Checklist 104=9 validées/95 ouvertes ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif). Writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, main/WAL/SHM, live WAL-index et ABA NOT_PROVEN, glib #160 OPEN_NOT_REMEDIATED. Protect main ACTIVE strict bypass=[] ; DRAFT/STOP MERGE jusqu'à CI HEAD exacte SUCCESS, vérification diff/reviews/threads puis squash expected_head_sha, postmain indépendante et #38 append-only.
