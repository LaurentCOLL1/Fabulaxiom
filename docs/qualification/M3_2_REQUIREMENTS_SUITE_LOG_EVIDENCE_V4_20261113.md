# Fabulaxiom M3.2 — V4, provenance des SUITES de tests Windows synthétiques

**13 novembre 2026 — CANDIDAT SOURCE-ONLY, PAS UNE ADMISSION.** Base protégée `main=de117648acde86d16c167964f902ad1b9e3179e3` après PR #353 MERGED par squash, Windows CI source [#43371849171](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43371849171) completed/SUCCESS au SHA `47ee4ac962dd9fbe5a80e59edcf4662cb6429d3f` ; postmain indépendante [#43454020652](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43454020652) EN COURS/NON QUALIFIÉE au checkpoint.

## Deux journaux distincts réellement consultés

| Tests de suite, React/Vitest non monté | Tâches candidates, toujours ouvertes | PR et SHA source exact | CI run et job Windows | Step CI | Résultat extrait du log |
|---|---|---|---|---|---|
| `src/m32WorldOrderIsolation.test.tsx` | M32-079, M32-082, M32-083 | #352, `a3462fa7097d398021a1f4104fe2a19a64c95654` | [#43318898667](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43318898667), job #131534076295 | 35 « Frontend tests » | `src/m32WorldOrderIsolation.test.tsx (6 tests)` — suite PASS |
| `src/m32WorldOrderBoundaries.test.tsx` | M32-075, M32-080 | #353, `47ee4ac962dd9fbe5a80e59edcf4662cb6429d3f` | [#43371849171](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43371849171), job #131709174580 | 35 « Frontend tests » | `src/m32WorldOrderBoundaries.test.tsx (5 tests)` — suite PASS |

Les deux jobs Windows sont `completed/success`, les étapes 35 sont `success` et les journaux du runner font apparaître ces lignes de suites. Le rapport V4 de la matrice ajoute un objet `synthetic_suite_observation` aux cinq exigences concernées, et uniquement à elles. Le validateur source-only `tools/test_m32_requirements_traceability.py` vérifie ces cinq correspondances, l'absence de faux statut de clôture, les locators et la séparation des anciennes preuves.

## Limitations explicites

Les nombres **6** et **5** désignent des agrégats de suites Vitest, **pas** des certificats par assertion, pas des observations de l'opérateur, pas des preuves de sécurité sur SQLite/Tauri/IPC ni des signatures des données historiques. En particulier `proof_audit.individual_test_step_result` reste `null` et `workflow_step_audit.job_id` reste `null` pour tous les 96 points ouverts, conformément au protocole existant. Aucun test P3v/P3w ne monte `App.tsx` ni n'écrit dans la base.

**M32-075, M32-078, M32-079, M32-080, M32-082, M32-083 restent [ ]. Checklist 104 : 8 closes / 96 ouvertes.** M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45 % estimés). PRODUCT_FIRST_PARALLEL_SAFETY maintenue. Writer/R1–R9 NOT_PROVEN ; P4 STOP ; G2B NOT_ACCEPTED ; G2C NOT_AUTHORIZED ; G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2) ; prospective NOT_STARTED ; main/WAL/SHM, WAL-index live et ABA NOT_PROVEN ; #35/#215 DRAFT, #36/#160 OPEN, glib Linux. STOP v6/v7, M:\\Fabulaxiom, Greenfield, backups, IPC writer, migration 007, Hello natif et recovery.

La qualification V4 exigera CI Windows au HEAD exact, reviews/threads, Protect main ACTIVE strict et zéro bypass, squash `expected_head_sha`, postmain indépendante, consignation append-only dans #38.
