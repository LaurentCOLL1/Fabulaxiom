> CHECKPOINT 08/11 : P3j #323 FUSIONNÉE sur `262c2490972c6eb60af175d1c9a6b3c9fa5c9420`, source CI #42496887886 SUCCESS au SHA exact ; parent postmain #42496034759 SUCCESS, nouveau postmain #42505241012 NON QUALIFIÉ à ce checkpoint. Les mentions CANDIDAT ci-dessous sont historiques, pas une admission writer/P4. #38 append-only #6724718276 ; PRODUCT_FIRST_PARALLEL_SAFETY et STOP inchangés.

# M3.2 P3j — propriétés de fiches fictives uni-latérales non comparables

8 novembre 2026 — **CANDIDAT NON QUALIFIÉ**. Parent protégé `main=af765376be38d2e34ebff4e8fb2533794d45222e` (#322), independent parent postmain Windows #42496034759 **À QUALIFIER**. Décision PRODUCT_FIRST_PARALLEL_SAFETY maintenue ; prévenir avant toute réorientation.

## Valeur produit et frontière

P3i montre les accords et les écarts littéraux de fiches inventées de deux romans, mais ne classe pas les fiches pour lesquelles aucune propriété `entity_id + property_key` n'est déclarée dans l'autre roman. P3j calcule `first_only` et `second_only` après la validation existante P3i, conserve chaque attribution `novel_id/scene_id/source_revision_id`, et affiche un fait « premier roman uniquement » ou « second roman uniquement ». Il n'infère **ni contradiction, ni accord, ni canon, ni date, ni absence de fait dans un roman réel**. L'absence d'entrée signifie seulement « non comparable dans les données déclarées ». Les accords et écarts précédents ne sont pas modifiés.

`src/M32P3fTwoNovelFictionalReview.tsx` : partition par clés explicites inventées, préservation des valeurs littérales et rendu JSX échappé. `src/m32P3fTwoNovelFictionalReview.test.tsx` : 3 tests nouveaux de non mutation/partition, refus d'une révision HEAD frauduleuse, refus sans fuite, échappement de l'entrée hostile. Pas d'App.tsx, route opérateur, import runtime, communication Rust/IPC ou SQL ; pas de changement de fixture existante, de workflow ni de dépendance.

**Attendus, NON PASS avant source Windows HEAD exact :** 332 Rust, 7 Greenfield, 69 inventaire SQLite, 183 continuité, **415 Vitest (412+3)**, 88/88 Chromium normal+CSP stricte, 25 blobs source Git de laboratoire. Parent postmain terminal SUCCESS exact SHA, propre CI Windows exacte, diff/reviews/threads, Protect main ACTIVE strict bypass=[], guarded squash expected_head_sha, postmain indépendant, issue #38 append-only.

**STOP maintenus :** M3.2 IN_PROGRESS_NOT_ACCEPTED ~45% estimés ; writer/R1–R9 NOT_PROVEN ; P4 réel STOP ; G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; main/WAL/SHM atomic custody et unseen ABA NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. Aucune base opérateur v6/v7, sauvegarde/journal, profil Greenfield existant, migration 007 runtime, native Windows Hello, marqueur/recovery. Les tests fictifs n'admettent aucun writer.
