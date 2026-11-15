# P3ai — Créations de précédences : cinq scénarios Chromium réels fictifs (15/11/2026)

## Parent et qualification
Parent `main=db1498c6a5ed86e894915b830e17c13dc364abbf` (#373 P3ah MERGED) ; CI source #43740585311 SUCCESS exact HEAD `6495b9e09f15bc22d31717d87b1ff8ac23427361`. Postmain indépendante #43741895550 **NON QUALIFIÉE au checkpoint**. P3ai DRAFT tant que parent postmain et sa propre CI Windows exacte ne sont pas terminales SUCCESS. Re-fetch protections reviews/threads, Protect main ACTIVE bypass=[], guarded squash expected_head_sha et nouvelle postmain obligatoire.

## Parcours réels Chromium sur données inventées
Le runner source Vite local exclusivement fictif exécute à nouveau les cas 1–92 et ajoute 5 parcours : 93 création C→D et impact explicite sur A/D vs A/B, avec confirmation uniquement RAM ; 94 refus d'un cycle C→A même pour comparaison D/A ; 95 refus d'une paire inversée doublonnée ; 96 retrait d'une paire invalide l'ancienne proposition et supprime le bouton de confirmation ; 97 changement d'Univers réinitialise les paires, les combobox et toute information précédente. Le même banc s'exécute sous Chromium dev et bundle CSP strict, boucle locale uniquement ; total **97/97 attendus, non qualifiés avant CI**. Aucune modification du code runtime de l'application, de SQLite réel, du writer ou de la navigation opérateur.

## Limites et STOP
M32-056/058/072/075/076/078/080/082/083 [ ] PARTIEL ; R4 M32-017/019/020 [ ]. Checklist 9/104 closes 95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %). PRODUCT_FIRST_PARALLEL_SAFETY. R1–R9 writer NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, main/WAL/SHM/ABA NOT_PROVEN, glib #160 OPEN. Aucune donnée opérateur, v6/v7, backup, Greenfield, IPC, 007, Hello ou recovery.
