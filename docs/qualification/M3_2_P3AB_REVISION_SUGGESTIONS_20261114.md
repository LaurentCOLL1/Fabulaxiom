# P3ab — suggestions d'identifiants de révisions fictives

**14 novembre 2026 — CANDIDAT TEST-ONLY NON QUALIFIÉ.** Parent main `8cba5e0bd758a39a501a5ee04c3957deec1ad36c` après #362 fusionnée, source Windows #43594666828 PASS HEAD exact ; postmain #43610824403 NON QUALIFIÉE au checkpoint.

## Contrat isolé

Dans `src/M32SyntheticEventExplorer.tsx`, après validation du graphe complet par `inspectM32Consultation`, les IDs `source_revision_id` non nuls et affichables dans la recherche de 256 unités UTF-16 sont dédoublonnés, classés par ordre Unicode scalaire et accompagnés de comptes purement fictifs d'ancres totales et historiques. Le `datalist` n'altère pas les sélections, les témoins, le graphe ni la pagination ; la recherche reste exacte et sensible à la casse, NFC/NFD distincts. Aucun rattachement réel à roman, chapitre, scène ou révision authentifiée n'est inféré.

## Tests candidats

Dix tests dans `src/m32ExplorerRevisionSuggestions.test.tsx` : identifiants distincts, comptes, tri et permutation, indépendance des filtres, casse, NFC/NFD, longueur, témoin explicite conservé, refus d'Universe étranger/Unicode malformé, échappement React des IDs hostiles, et absence d'écriture/persistance. Aucun PASS CI au HEAD de P3ab encore acquis.

M32-071/075/078/081/082 [ ], checklist 104 = 8 closes/96 ouvertes ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %). PRODUCT_FIRST_PARALLEL_SAFETY et tous STOP writer/R1–R9, P4/G2/G3, originaux v6/v7, WAL/SHM/ABA et glib #160 maintenus. Aucun App.tsx, Tauri, SQLite, IPC, fichier ou réseau.
