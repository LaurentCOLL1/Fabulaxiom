# P3ah — impacts des nouvelles précédences fictives choisies (15 novembre 2026)

## Parent et sécurité
Parent `main=c206d578ca53657ec610f3b197cc3918b27198de`, #372 R4 MERGED, source Windows #43724709726 SUCCESS au HEAD exact `32bdc62d616202d87d8c61881118dc7f2b2cb4df`, postmain indépendante #43739867338 PENDING/NON QUALIFIÉE au checkpoint de préparation. Candidat P3ah NON QUALIFIÉ avant CI propre sur HEAD exact, parent postmain SUCCESS, reviews/threads, Protect main ACTIVE strict `bypass_actors=[]`, expected_head_sha et postmain indépendante.

## Fonction utilisateur expérimentale
Dans le laboratoire React M3.2 non monté dans App.tsx, l'auteur peut proposer un lot de 1–16 précédences fictives puis choisir jusqu'à 8 paires d'ancres à comparer. La lecture avant/après explicite les relations modifiées, témoins minimaux et les paires inchangées, sans chronologie mondiale exhaustive. Prévisualisation pure en RAM ; confirmation humaine distincte et seule en mémoire ; aucune sauvegarde. Les entrées historiques, étrangères, mal formées, doublonnées, cycles et commandes falsifiées sont refusées.

## Preuves candidates
12 nouveaux cas Vitest `src/m32FictionalCreatedBatchImpact.test.tsx` : chaîne transitive créée, paire non touchée, inversion directionnelle, doublons inverses, limite et champs falsifiés, IDs historiques/étrangers, Unicode, cycle global même hors paire, origine opérateur forgée, immutabilité baseline, absence d'ordre récit/révélation et rendu de l'UI sans faux succès.

## Limites
M32-056/058/072/075/076/078/080/082/083 [ ] PARTIEL ; R4 M32-017/019/020 [ ]. Checklist 9/104, M3.2 IN_PROGRESS_NOT_ACCEPTED (~45 %). PRODUCT_FIRST_PARALLEL_SAFETY. Writer R1–R9 NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, glib #160 OPEN. Aucune donnée réelle ni migration, IPC, Hello, Greenfield, backup ou recovery.
