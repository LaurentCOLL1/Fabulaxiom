# P3af — Comparaison de paires choisies après correction fictive (15/11/2026)

## Sécurité et parent
Parent main `867c02902fbe732a5b89fc06024d0fdfd6c3140c` après PR #369 MERGED ; source Windows #43700531238 SUCCESS au HEAD exact, postmain #43718729742 **PENDING / NON QUALIFIÉE au checkpoint de préparation**. P3af CANDIDAT ; exiger son CI Windows au HEAD exact, Protect main ACTIVE `bypass_actors=[]`, reviews/threads, postmain parent SUCCESS, guarded squash avec `expected_head_sha` et postmain indépendante avant toute qualification.

## Fonction
Laboratoire React fictif NON MONTÉ : 1 à 8 paires d'ancres choisies explicitement par l'auteur. Comparaison avant/après des relations et chaînes témoins minimales, avec comptage des relations modifiées et des témoins modifiés. Orientation et ordre de sélection préservés. Aucun balayage global, aucune relation inventée ou inférence d'ordre total.

## Tests candidats
12 cas Vitest dans `src/m32FictionalSelectedPairsImpact.test.tsx` : paires impactées et non impactées, témoin changé sans changement de relation, orientation, doublon inverse, limite, champs forgés, IDs étrangers/historiques, Unicode mal formé, cycle hors sélection, refus source non fictive, baseline immuable, provenance read-only, interface sans faux succès de sauvegarde.

## Limites
Aucune base v6/v7, Greenfield, backup, IPC, SQLite, writer, 007, Hello ou recovery. R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, glib #160 OPEN. M32-072/073/078/080/081/083 [ ] PARTIEL ; R4 M32-017/019/020 [ ]. Checklist 9/104 closes 95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45%). PRODUCT_FIRST_PARALLEL_SAFETY maintenue.
