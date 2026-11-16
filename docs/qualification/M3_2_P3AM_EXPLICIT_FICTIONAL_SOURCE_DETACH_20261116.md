# P3am — détachement explicite d'une source fictive (16 novembre 2026)

## Produit
Dans `M32ManualChronologyLab.tsx` (atelier synthétique non monté), la correction d'une ancre active propose une case à cocher explicite « Détacher explicitement la source historique de la version proposée ». Le choix est désactivé tant qu'aucune ancre n'est sélectionnée ; changer l'ancre désélectionne le choix. Le changement annule la prévisualisation existante et exige une nouvelle revue avant confirmation. Seul `correctionInput` passe `source_scene_id:null` et `source_revision_id:null` ; l'ajout d'une ancre conserve son entrée indépendante. L'ancienne ancre historique garde `source_revision_id` : aucun effacement des sources authentiques n'est possible par cet atelier.

## Preuves candidates
Test Vitest n°25 : contrôle de rendu et absence de fausse sauvegarde. Chromium n°99 : case initialement désactivée, sélection d'une ancre, prévisualisation annulée au changement, nouvelle revue, confirmation en RAM sans sauvegarde. **Non qualifié avant CI Windows source HEAD exact**. Aucune autorisation de writer, Tauri IPC, stockage opérateur, v6/v7, Greenfield, recovery, Hello, schéma SQL, migration 007 ou backup.

## Gates
Parent `main=f74ced069e1b646b9ed4a2fdcb74dbe775b7d142` ; #380 MERGED, CI source Windows #43939041031 SUCCESS exact `2507c1d57895272adb1f03fd28d3e633c4e78105` ; postmain #43941220413 PENDING_UNQUALIFIED au checkpoint. Checklist 104=9 closes/95 ouvertes, M32-055/059/061/073/075/076/079/081 [ ] PARTIELS, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 % indicatif), PRODUCT_FIRST_PARALLEL_SAFETY. R1–R9/writer NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, main/WAL/SHM/ABA NOT_PROVEN, glib #160 OPEN. Aucune fusion avant postmain parent SUCCESS exact, CI P3am terminale au HEAD exact, checks/reviews/threads, Protect main ACTIVE bypass=[], guarded squash expected_head_sha, postmain indépendante et journal #38 append-only.
