# P3bm — révision source historique liée ou absente (21/11/2026)

Atelier React fictif **NON MONTÉ** : filtre « Toutes / Avec révision source explicite / Sans révision source explicite ». Une version sans `source_revision_id` peut conserver son `anchor_id` : absence de source ≠ absence d'ancre ≠ temps unknown. Les critères source, roman, scène, ancre, date, calendrier, type temporel et liaison doivent correspondre **à la même version historique**, jamais à un mélange de versions. Changement de filtre efface page et sélection ; reset P3bh efface aussi source-link, valeurs invalides refusées. Aucun motif ou note non sélectionné n'est exposé.

Vitest #47 tests d'invariants, filtre contradictoire, tombstone et immutabilité ; Vitest #48 SSR aucune fuite ; Chromium #110 étendu pour choisir liaisons et reset. **CANDIDATS avant CI HEAD exact de la branche.** Parent main `57a43c397b831f2f336a6fd9ee3837ea25a761c2`, PR #407 source CI #44913548368 PASS `68a76ef5c12f90a6a1e6fd9375a35c39c8658e19`, postmain indépendante #44917189406 PASS event push SHA exact main.

M32-071/075/078/081 [ ] ; checklist 104=12/92 ; M3.2 IN_PROGRESS_NOT_ACCEPTED, PRODUCT_FIRST_PARALLEL_SAFETY. Aucune entrée App.tsx/Tauri/SQLite/writer/opérateur. STOP Writer/R1–R9 NOT_PROVEN, R3 partiel, D3c conception, G3 STOP_UNAVAILABLE, live SQLite WAL-index/ABA NOT_PROVEN.
