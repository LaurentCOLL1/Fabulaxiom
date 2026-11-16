# P3ak — provenance historique entre deux romans fictifs (16 novembre 2026)

## Objet et portée
Six tests Vitest nouveaux (cas 14–19) vérifient la conservation de l'identifiant exact de révision d'une ancre remplacée, le changement volontaire de scène/révision entre deux romans fictifs d'un même univers, le refus d'une scène et d'une révision discordantes, le rejet d'une révision étrangère/inconnue, le refus de confirmer une prévisualisation devenue périmée et un détachement explicite de source sans effacer celle de la version historique. Le travail concerne `src/m32FictionalAnchorSupersessionPreview.test.tsx` : **fixture React locale non montée**, sans modifier le writer, SQLite original, App.tsx, Tauri IPC ni les sauvegardes.

## Qualification à venir
Parent protégé `main=4fce362a1cf7ee2093b31cf30f660bedbe670e1c`, #378 MERGED avec CI source Windows #43918290940 completed/SUCCESS HEAD exact `6d0fe82efb5d8d3b30d80e7b7922c053c5e70555`, postmain #43928986885 PENDING_UNQUALIFIED au pointage ; source P3ak `42e1607b8dfa13f32c860e89488a0f2373e0f685` NON QUALIFIÉE. Avant fusion : exiger postmain parent SUCCESS exact, CI Windows P3ak terminal SUCCESS propre au nouveau HEAD, diff/reviews/threads, Protect main ACTIVE bypass=[], squash `expected_head_sha`, postmain et journal #38 append-only.

## Limites
Checklist M3.2 104 = 9 closes/95 ouvertes ; M32-055/059/061/073/075/076/079/081 restent [ ] PARTIELS ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY. Writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, main/WAL/SHM, live WAL-index et ABA NOT_PROVEN ; glib #160 OPEN. STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
