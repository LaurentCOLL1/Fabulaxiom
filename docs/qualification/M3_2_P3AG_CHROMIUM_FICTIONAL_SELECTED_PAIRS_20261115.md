# P3ag — Parcours utilisateur multi-paires sous Chromium réel fictif, 15/11/2026

## Parent et preuve
Parent `main=eedf2f571ea3e4e07da4fd992dae515515c016a8` après #370 MERGED, source Windows #43719583953 terminal SUCCESS au HEAD exact `0e17d38fe30fab1329830ee818dd613b28805b42`. Postmain indépendante #43722727745 **NON QUALIFIÉE au checkpoint de création** ; exiger résultat terminal SUCCESS au parent avant fusion. PR candidate P3ag = NON QUALIFIÉE jusqu'à CI Windows au HEAD exact, reviews/threads, Protect main ACTIVE `bypass_actors=[]`, `expected_head_sha` et postmain indépendante.

## Scénarios navigateur inventés
Quatre nouveaux cas Chromium (89–92) exécutés deux fois : Vite dev local et bundle compilé sous CSP strict. (89) Révocation d'un lien humain fictif, sélection explicite de A/C et A/B, une relation/témoin changé et l'autre inchangé, confirmation RAM et absence de faux succès de sauvegarde. (90) Sélection inversée C/A refusée comme doublon de A/C. (91) Retrait d'une paire après prévisualisation invalide la confirmation périmée. (92) Changement d'univers fictif efface les paires et la sélection précédente. Aucun véritable navigateur opérateur ni App.tsx monté.

Le banc d'essai existant garde les contraintes de scénario inventé, source Vite non-produit, écoute uniquement sur 127.0.0.1, politique CSP et interdiction de réseau hors boucle locale. Les tests 89–92 font passer le total candidat à 92/92 (sous réserve de réussite CI exacte). Aucun SQLite original, IPC, writer, Tauri, import App, Hello, migrations, backups ou recovery.

## Statuts
M32-072/073/075/076/078/080/081/082/083 [ ] PARTIEL ; R4 M32-017/019/020 [ ]. Checklist 9/104 closes, 95 ouvertes, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %). PRODUCT_FIRST_PARALLEL_SAFETY inchangée ; R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; glib #160 OPEN.
