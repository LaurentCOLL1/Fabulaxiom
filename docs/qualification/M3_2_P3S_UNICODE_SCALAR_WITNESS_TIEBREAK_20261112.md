# M3.2 P3s — témoin Unicode scalaire déterministe (CANDIDAT)

12 novembre 2026 — parent `main=33d701cc372c50178e8d9b0839761a77a1514652`, #344 MERGED, CI Windows source #43117900804 SUCCESS, postmain #43154409245 EN COURS/NON QUALIFIÉE au checkpoint.

L'aperçu React `M32WorldOrderComparison` est non monté et ne manipule que des fixtures fictives. Son choix illustratif parmi les chaînes de précédence humaines actives de longueur minimale utilise maintenant l'ordre lexicographique des **points de code Unicode** des identifiants d'arêtes, au lieu de la collation locale `localeCompare`. Tests : Z/a (U+005A/U+0061), U+E000 / U+1F4A0, permutation d'insertion et rejet d'une précédence révoquée. Le tri des témoins n'est ni un ordre du monde total ni une revendication de parité Python Stage25/26 ; sélection filtrée et autres écarts restent ouverts.

**P3s NON QUALIFIÉ** avant CI Windows terminale HEAD exact, reviews/threads, Protect main strict `bypass_actors=[]`, squash `expected_head_sha`, postmain indépendante et #38 append-only. Checklist 104 : 7 closes, 97 ouvertes ; M32-058/080 [ ]. PRODUCT_FIRST_PARALLEL_SAFETY maintenue ; M3.2 IN_PROGRESS_NOT_ACCEPTED (~45%), writer/R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, glib #160 OPEN. Aucun opérateur SQLite, M:\Fabulaxiom, Greenfield existant, backups, IPC writer, 007, Hello natif ou recovery.
