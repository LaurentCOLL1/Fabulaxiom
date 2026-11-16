# P3aj — Revoir et confirmer une correction d'ancre fictive (16 novembre 2026)

## Parent et preuve
Parent `main=729d6860b1bbce9d08f5b464070ea3edb008e273` (#376 M32-005 MERGED). Source Windows #43804081056 completed/SUCCESS au HEAD exact `fb63521916281c1e9fdbdfa16f04c8cf3726ee23`. Postmain indépendante #43805234690 PENDING_UNQUALIFIED au checkpoint de préparation : ne pas qualifier P3aj avant CI de sa propre tête, postmain parent, Protect main ACTIVE bypass=[], reviews/threads, guarded squash expected_head_sha et postmain indépendante.

## Portée et refus
Nouveau module `src/m32FictionalAnchorSupersessionPreview.ts` : copie immuable des avant/après, préservation des ancres historiques, type temporel explicite (exact/approximatif/relatif/inconnu), rejet d'une correction sur ancre absente/historique ou ayant des précédences actives, absence d'inférence grégorienne ou d'ordre global. Confirmation revalide intégralement l'état actuel en RAM et refuse previews forgées/périmées. Dans `src/M32ManualChronologyLab.tsx`, le bouton d'application directe est remplacé par une prévisualisation avant/après et confirmation séparée. Toute modification des champs invalide la prévisualisation. Tous les composants restent inaccessibles via App.tsx de production.

13 tests Vitest nouveaux et un cas réel Chromium n°98 : changement de type temporel invalide la confirmation. Cas historique Chromium n°45 adapte la correction à l'approbation explicite. Les 98 cas s'exécutent normalement et sous CSP strict uniquement sur le navigateur fictif local (attendus non qualifiés avant CI).

## Gates
M32-055/059/061/073/075/076/079/081 restent [ ] partiels ; checklist 9 closes / 95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %), PRODUCT_FIRST_PARALLEL_SAFETY. Aucun writer/R1–R9, P4, G2B/C/G3, SQLite source, profil Windows, v6/v7, sauvegarde, migration 007, Hello ou recovery. glib #160 OPEN ; atomicité main/WAL/SHM/ABA NON PROUVÉE.
