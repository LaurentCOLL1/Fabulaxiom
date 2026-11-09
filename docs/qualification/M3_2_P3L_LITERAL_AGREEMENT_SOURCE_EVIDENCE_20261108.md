> CHECKPOINT P3l #327 FUSIONNÉE : `main=8d69691d173abda2a6b448171d91833ffdff4445`, source Windows #42532875576 terminal SUCCESS SHA exact (332 Rust/421 Vitest/88 Chromium normal+CSP), parent #326 postmain #42530167231 attempt 2 terminal SUCCESS même SHA après failure transient non expliqué attempt 1. Nouveau postmain #42559103573 EN COURS/NON QUALIFIÉ. Les mentions CANDIDAT ci-dessous restent historiques et ne constituent aucune admission writer/P4. #38 append-only #6731872221 ; PRODUCT_FIRST_PARALLEL_SAFETY et STOP inchangés.

# M3.2 P3l — accords littéraux déclarés, sources historiques visibles

8 novembre 2026 — **CANDIDAT NON QUALIFIÉ**. Parent protégé `main=ba8a21a2e758f25a0240c729797add551358239d` (#326). Postmain indépendant #42530167231 **attempt 1 FAILURE**, `WebSocket closed without opened.` côté Chromium Vite-HMR après 48 scénarios PASS, étapes suivantes SKIPPED ; **attempt 2 completed/SUCCESS au SHA exact, 87 étapes Windows PASS**, même commit et mêmes gates. L'instabilité éventuelle reste tracée dans #38 ; aucune exception ni affaiblissement de tests. PRODUCT_FIRST_PARALLEL_SAFETY maintenue, prévenir AVANT changement.

## Valeur produit

P3i compare les valeurs déclarées, P3j classe les propriétés sans correspondant et P3k autorise la sélection d'un personnage inventé. L'interface comptait les accords mais n'en affichait pas le détail, contrairement aux écarts. P3l montre chaque **accord littéral déclaré** avec `entity_id`, `property_key`, valeur **identique**, les deux `novel_id` et les deux `source_revision_id` historiques inventés. Le filtre P3k s'applique aussi aux accords, sans altérer les écarts ou faits unilatéraux. La validation des deux romans et de leurs révisions précède le rendu ; une valeur identique ne constitue PAS une preuve de canon ni de cohérence générale.

## Périmètre et tests

Seulement `src/M32P3fTwoNovelFictionalReview.tsx` et `src/m32P3fTwoNovelFictionalReview.test.tsx` avec trois nouveaux tests Vitest : (19) affiche exactement la valeur commune et les deux révisions historiques sans mutation, (20) n'affiche aucun accord pour deux valeurs divergentes, (21) échappe un littéral HTML hostile et refuse une attribution historique falsifiée AVANT divulgation. Aucun `App.tsx`, route réelle, Tauri IPC, SQL runtime, dépendance, lockfile, workflow, profil opérateur ni writer.

**Attendus (NON PASS avant Windows CI terminale HEAD exact) :** 332 Rust, 7 Greenfield, 69 inventaire SQLite, 183 continuité, **421 Vitest** (418+3), Chromium 88/88 normal et 88/88 strict CSP, 25 blobs Git de laboratoire fictif. Contrôler CI source, fichiers/reviews/threads, Protect main ACTIVE strict bypass=[], guarded squash `expected_head_sha`, postmain indépendant et issue #38 append-only.

## STOP

M3.2 IN_PROGRESS_NOT_ACCEPTED (~45% estimation d'ingénierie), writer/R1–R9 NOT_PROVEN, vrai P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE ; historique PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED ; custody atomique main/WAL/SHM et ABA invisible NOT_PROVEN ; glib #160 OPEN_NOT_REMEDIATED. Ne toucher ni v6/v7 opérateur, ni profil Greenfield existant, sauvegardes/journaux, writer IPC, migration 007, Hello natif, marqueur/recovery. CI fictive ≠ admission.
