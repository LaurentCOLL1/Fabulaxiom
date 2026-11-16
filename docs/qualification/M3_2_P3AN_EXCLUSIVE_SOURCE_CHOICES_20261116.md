# P3an — choix de provenance fictive non ambigus (16 novembre 2026)

## Produit et sûreté
Dans `M32ManualChronologyLab.tsx` (atelier navigateur exclusivement fictif), sélectionner une nouvelle scène annule explicitement le détachement de la source, remet la sélection de révision à zéro et invalide la prévisualisation. Inversement, activer le détachement efface la scène et sa révision proposées, en conservant l'ancre historique ; tout changement invalide la prévisualisation et exige une nouvelle revue. La correction conserve les refus du reducer et ne permet aucune sauvegarde. Les deux choix ne peuvent plus rester contradictoires.

## Preuves candidates
Vitest n°26 : signalement UI de l'exclusivité sans sauvegarde ; Chromium #100 : détachement puis scène avec révision exacte, provenance réaffirmée ; Chromium #101 : sélection de scène/révision puis détachement explicite, valeurs effacées et confirmation RAM. Total Chromium attendu 101/101, **NON QUALIFIÉ jusqu'au SUCCESS réel sur HEAD P3an exact**. Uniquement données fictives, pas d'App.tsx production, Tauri IPC, writer, migration, original, profil, backup, Windows Hello ou recovery.

## Gates
Base `main=800b6680d8cddb52aa9a57b87b7d53cd6a0e171a`, PR #381 source CI Windows #43942337234 completed/SUCCESS HEAD exact `7711a270a5fdf48d64f54643332ea9c477c32049` et fusion protégée ; postmain indépendante #43955730862 PENDING_UNQUALIFIED à la préparation. Checklist 104 = 9 closes / 95 ouvertes, M32-055/059/061/073/075/076/079/081 [ ] PARTIELS, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY, writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, main/WAL/SHM, live WAL-index et ABA NOT_PROVEN ; glib #160 OPEN. Pas de fusion avant parent postmain SUCCESS exact, propre CI Windows source P3an SUCCESS HEAD exact, reviews/threads et Protect main ACTIVE strict bypass=[], squash expected_head_sha, postmain indépendante, journal #38 append-only.
