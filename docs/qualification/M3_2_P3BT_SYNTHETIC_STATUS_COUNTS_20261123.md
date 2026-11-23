# P3bt — décompte des statuts de l'explorateur fictif (23/11/2026)

**SOURCE_ONLY_CANDIDATE_UNQUALIFIED ; NO_AUTO_ACCEPTANCE ; NO_RUNTIME_ADMISSION.** Parent protected main=de4b1fd9415d985d0dc13b47952d1fe908e5ffcd, #423 MERGED, postmain indépendante #45239305602 completed/SUCCESS sur SHA exact parent, Windows 93/93. Journal #38 #7110312015 append-only.

## Portée produit isolée
L'explorateur React fictif non monté affiche current/revoked/superseded et le total calculés après validation du graphe complet, avant tout filtre. Ces nombres sont stables pendant les recherches, les filtres de statut, de révision exacte et la pagination. Ils ne valident ni source SQLite ni provenance d'une scène.

## Tests candidats
Cinq scénarios Vitest dans src/m32ExplorerStatusSummary.test.tsx : partition totale, indépendance des filtres, veto des cycles cachés, refus inter-Univers, affichage accessible et échappement HTML sans mutation. La CI Windows pull_request HEAD exacte reste à qualifier. Aucun fichier, réseau, Tauri, SQLite, runtime ou persistance touché.

**M32-071 [ ] / M32-075 [ ] / M32-078 [ ] / M32-081 [ ] OPEN_NOT_ACCEPTED.** Checklist 104 : 13 CLOSED_SCOPED / 91 OPEN_NOT_ACCEPTED. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% indicatif), PRODUCT_FIRST_PARALLEL_SAFETY ; PR #35/#215 DRAFT NON_ADMITTED.

STOP Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; PENDING_EXTERNAL_ATTESTATION(21/3/2) prospective NOT_STARTED ; R2 STOP/R3 partiel/D3c conception/D3b-4/5 et D3b-5 STOP ; main/WAL/SHM, live SQLite WAL-index et ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED ; STOP v6/v7, M:\Fabulaxiom, Greenfield, backups, IPC writer, 007, Hello, recovery.
