# M32-072 — témoins exacts de refus par lot fictif (24/11/2026)

Parent main 41801b5b792b8204e8aabfc555ec63a8b62b6242 ; #427 MERGED source #45429799963 PASS exact HEAD a5523b4b1d094396775c0d5b4739e1d107644996 ; postmain #45469647606 PASS exact main. 16/88 ; IN_PROGRESS_NOT_ACCEPTED ; PRODUCT_FIRST_PARALLEL_SAFETY.

## Preuve candidate
Le laboratoire non monté M32FictionalHumanOrderBatchLab présente déjà les sélecteurs humains, raisons, propositions, paires d'impact choisies, simulation avant/après, puis confirmation explicite en RAM. Le moteur de lot réutilise maintenant la prévisualisation de précédence pour nommer le rang de la proposition refusée et les IDs témoins exacts (y compris les liens proposés plus tôt dans le lot, jamais appliqués). Le rôle alert existant affiche cette explication ; aucun accès persistant. Les tests 19–22 vérifient cycle tardif, témoin existant, doublon et référence historique sans mutation. Aucun PASS candidat avant CI HEAD exacte. M32-072 reste ouverte jusqu'à revue de la preuve complète.

## M32-070 en parallèle — audit de conception
M32ManualChronologyLab propose type de date, calendrier saisi, libellé, précision et révision source explicite ; M32FictionalEventManualWorkshop propose titre, note, ancre et révision. Ces contrôles ne démontrent pas à eux seuls la création d'un calendrier distinct, sa validité et l'ensemble du parcours manuel sans IA. Garder M32-070 ouverte. M32-078 demeure ouverte, aucun changement aux compteurs ni au registre accepté. Toutes interdictions STOP inchangées, G3 STOP_UNAVAILABLE ; aucun writer, runtime, original ou admission opérateur.
