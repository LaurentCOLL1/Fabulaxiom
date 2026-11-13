# M3.2 P3w — limites de volume, refus global et précédences historiques (test-only)

**13 novembre 2026 — CANDIDAT, AUCUNE ADMISSION.** Parent protected `main=d51505ff8a08d89e5ded7b92ef65a72f7c8e3e90` après #352 P3v MERGED ; CI source Windows [#43318898667](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43318898667) attempt 1 completed/SUCCESS HEAD exact `a3462fa7097d398021a1f4104fe2a19a64c95654`, 441 Vitest frontend dont six P3v, job Windows 92 étapes. Postmain indépendante [#43371248337](https://github.com/LaurentCOLL1/Fabulaxiom/actions/runs/43371248337) EN COURS/NON QUALIFIÉE au checkpoint.

## Périmètre nouveau et reproductible

`src/m32WorldOrderBoundaries.test.tsx` crée un Universe inventé avec **512 ancres** et **2048 relations** actives, orientées sans cycle, et contrôle comparaison directe, inversion et résultat `same`, raison humaine, preuve stable et immutabilité malgré l'ordre des lignes inversé. Des fixtures volontairement invalides dépassent les plafonds avec **513 ancres**, **2049 précédences** (dont une révoquée) ou **2049 scènes** : aucune comparaison partielle, motif historique ni scène inventée ne doivent apparaître dans HTML. Une back-edge active créant un cycle au plafond de 2048 impose un refus global, y compris pour la comparaison identité. Une back-edge **révoquée** n'entre jamais dans le graphe courant et ne crée pas une relation fictive.

Le banc n'utilise que React/Vitest synthétique **non monté** ; aucune modification à `App.tsx`, SQLite, Rust, Tauri, profils utilisateur, réseau, IPC, backup, migration 007 ni recovery.

## Statut et frontière

**M32-075/080 restent [ ]** : le banc réduit le risque de faux affichage au plafond mais ne prouve pas l'accessibilité utilisateur complète, le serveur hors ligne, les transactions, les droits Windows, l'atomicité des sidecars ni la sûreté du writer. Checklist : **104 tâches, 8 closes et 96 ouvertes** ; M3.2 `IN_PROGRESS_NOT_ACCEPTED` (~45% estimés), PRODUCT_FIRST_PARALLEL_SAFETY inchangée. R1–R9/writer NOT_PROVEN, P4 STOP, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, attestations historiques PENDING_EXTERNAL_ATTESTATION(21/3/2), prospective NOT_STARTED, main/WAL/SHM/WAL-index live/ABA NOT_PROVEN ; #35/#215 DRAFT, #36/#160 OPEN glib Linux. Aucun accès aux données opérateur.

Qualification requise : CI Windows au HEAD exact terminale, reviews/threads, Protect main ACTIVE strict bypass=[], squash expected_head_sha, postmain indépendante et journal #38 append-only.
