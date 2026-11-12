# M3.2 P3t — Oracle fini indépendant de précédence (CANDIDAT)

**12 novembre 2026, CANDIDAT TEST-ONLY**, parent protected `main=c2fedec22778812db21486b4c2dbba7cf39b6cb6`. #348 MERGED (source Windows CI #43246445107 attempt 1 completed/SUCCESS au HEAD exact `f9e707f1dd208bf3b0b0fcfbe7b5d7bf98d0cfbc`) ; sa postmain indépendante #43295484390 **EN COURS/NON QUALIFIÉE au checkpoint**.

## Risque réduit

Le prototype React M32WorldOrderComparison choisit une chaîne justificative humaine parmi les précédences actives sur des données fictives. P3t ne modifie pas son runtime. Le nouveau test `src/m32WorldOrderComparison.test.tsx` explore exhaustivement **2^10 = 1024 DAG** obtenus avec toutes les sous-combinaisons des dix relations orientées de cinq assertions (A–E). Il ajoute une relation directe historique **révoquée** et compare A vers E ainsi que E vers A ; il répète chaque cas avec les arêtes réordonnées. L'oracle est distinct de l'implémentation : énumération de tous chemins, sélection longueur minimale, puis identifiants de relation ASCII croissants. Le témoin doit rester exact ; les graphes déconnectés doivent rester incomparables, et les snapshots restent immuables. Aucun calendrier ni narration ne sert d'ordre implicite.

## Frontières

Les 1024 cas représentent seulement des fixtures inventées, dans un seul Universe et sans connexion SQLite/Tauri, sans admission writer. Ils **ne couvrent pas** la parité Python Stage25/26 complète, la prévention runtime de tous conflits, les permissions système, la persistance/revocation/rollback atomique ou une recette Windows opérateur. **M32-080 reste [ ]**, comme M32-078. Checklist 104 : 8 closes / 96 ouvertes. M3.2 IN_PROGRESS_NOT_ACCEPTED (~45%), PRODUCT_FIRST_PARALLEL_SAFETY conservée ; R1–R9 NOT_PROVEN, G2B NOT_ACCEPTED, G2C NOT_AUTHORIZED, G3 STOP_UNAVAILABLE, P4 STOP, #36 attestations OPEN, #160 glib Linux OPEN.

Qualification requise : CI Windows au HEAD exact, reviews/threads, Protect main ACTIVE strict bypass=[], squash expected_head_sha, CI postmain indépendante et journal #38 append-only. STOP v6/v7 réels, M:\Fabulaxiom, Greenfield existant, backups, IPC writer, migration 007, Hello natif, recovery.
