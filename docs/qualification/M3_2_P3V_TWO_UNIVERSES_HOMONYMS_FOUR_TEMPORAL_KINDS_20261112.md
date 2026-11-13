# M3.2 P3v — deux Universes fictifs, homonymes et quatre temporalités

**12 novembre 2026 : CANDIDAT TEST-ONLY, SANS ADMISSION.** Parent protégé `1e85594dde1080c43c0a22509d962f732d08a4e2`, #351 MERGED, source CI Windows #43315035856 completed/SUCCESS HEAD exact `587085e38523448e0a1a076ceff2f9de6627ef5c`, postmain #43317923849 **EN COURS/NON QUALIFIÉE au checkpoint**.

## Portée de preuve

Le fichier `src/m32WorldOrderIsolation.test.tsx` crée deux Universes indépendants, avec mêmes IDs d'ancres, précédences, scènes et romans. Chacun conserve sa relation active A→B→C et D incomparable. Les chaînes de motifs doivent rester issues du bon Universe ; toute injection d'ancre, précédence ou scène étrangère est refusée globalement, sans conclusion partielle ni fuite de motif. Un doublon **dans le même Universe** est refusé, même lorsque deux Universes distincts autorisent des IDs homonymes.

Un second banc remplace la temporalité de A par chacun des quatre modes exact/approximate/relative/unknown, change ses calendriers et références de révision fictifs, inverse les deux romans et leurs positions de narration. Aucune nouvelle relation du temps du monde n'est inférée ; les comparaisons explicites restent fondées uniquement sur les précédences humaines actives. Ordre de révélation non rédigé, snapshots inchangés, aperçus en lecture seule. Le test n'utilise pas de base réelle, d'application montée, d'IPC ni de réseau.

**Limites non franchies :** fichiers source/migration 007, SQLite, writer/R1–R9, isolation de stockage authentique, parité complète Python Stage25/26, rollback et recette Windows opérateur. **M32-079/082/083 [ ] ; M32-078/080 [ ]** ; 104 tâches : 8 closes / 96 ouvertes. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45%), PRODUCT_FIRST_PARALLEL_SAFETY inchangée. Qualifier CI Windows HEAD exact, reviews/threads, Protect main ACTIVE strict bypass=[], squash expected_head_sha, postmain indépendante, #38 append-only. #35/#215 DRAFT et #36/#160 OPEN, tous STOP maintenus.
